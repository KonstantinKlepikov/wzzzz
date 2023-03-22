from magic_filter import F
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery
from app.schemas.scheme_errors import HttpError
from app.middleware.api_queries import QuerieMaker
from app.keyboards.templates_kb import (
    TemplatesCallbackFactory,
    update_choice_text_fab,
    get_templates_keyboard_fab
        )


router = Router()
user_data = {}


@router.message(Command('get_vacancies'))
async def get_vacancies(message: Message, qm: QuerieMaker) -> None:
    """Show user templates names and add interfase
    for vacancy query with template
    """
    user_id = message.from_user.id
    user_data[user_id] = '-'
    try:
        result = await qm.get_templates_names(user_id)
        if result['names']:
            await message.answer(
                f'Choose template for query: -',
                reply_markup=get_templates_keyboard_fab(
                    '|'.join(t['name'] for t in result['names'])
                        )
                    )
        else:
            await message.answer('Templates not found. Add with /create template_name')
    except HttpError as e:
        await message.answer(e.message)


@router.callback_query(TemplatesCallbackFactory.filter(F.action == "change"))
async def callbacks_template_change_fab(
    callback: CallbackQuery,
    callback_data: TemplatesCallbackFactory
        ):
    """Fix chooosen tevplate callback
    """
    user_id = callback.from_user.id
    user_data[user_id] = callback_data.templ
    await update_choice_text_fab(
        message=callback.message,
        templ=callback_data.templ,
        templates=callback_data.templates,
            )
    await callback.answer()


@router.callback_query(TemplatesCallbackFactory.filter(F.action == "finish"))
async def callbacks_template_finish_fab(callback: CallbackQuery):
    """Query with template callback
    # TODO: change me
    """
    user_templ = user_data.get(callback.from_user.id, '-')

    await callback.message.edit_text(f"Your choice: {user_templ}")
    await callback.answer()


@router.message(Command('create'))
async def create_template(
    message: Message,
    command: CommandObject,
    qm: QuerieMaker
        ) -> None:
    """Create new clear template with given name
    """
    user_id = message.from_user.id
    if command.args:
        try:
            await qm.create_template(user_id, command.args)
            await message.answer(f'Is created template: \n{command.args}')
        except HttpError as e:
            await message.answer(e.message)
    else:
        await message.answer(
            'Use /create template_name'
            '\n<i>(no more than 20 characters, only ascII letters or numbers)</i>',
            parse_mode="HTML"
                )
