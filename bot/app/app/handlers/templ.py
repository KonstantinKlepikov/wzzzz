from magic_filter import F
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from app.schemas.scheme_errors import HttpError
from app.middleware.api_queries import QuerieMaker
from app.keyboards.templates_kb import (
    TemplatesCallbackFactory,
    update_choice_text_fab,
    get_templates_keyboard_fab
        )


router = Router()


class StateStorage(StatesGroup):
    template = State()


@router.message(Command('templates'))
async def get_templates_names(message: Message, qm: QuerieMaker) -> None:
    """Show available user templates names
    """
    user_id = message.from_user.id
    try:
        result = await qm.get_templates_names(user_id)
        if result['names']:
            names = '\n'.join(t['name'] for t in result['names'])
            await message.answer(f'Available templates:\n{names}')
        else:
            await message.answer('Templates not found. Add with /create template_name')
    except HttpError as e:
        await message.answer(e.message)


@router.message(Command('get_vacancies'))
async def get_vacancies(message: Message, qm: QuerieMaker, state: FSMContext) -> None:
    """Show user templates names and add interfase
    for vacancy query with template
    """
    user_id = message.from_user.id
    await state.set_state(StateStorage.template)
    await state.update_data(template='-')
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
    callback_data: TemplatesCallbackFactory,
    state: FSMContext,
        ):
    """Fix chooosen tevplate callback
    """
    await state.update_data(template=callback_data.templ)
    await update_choice_text_fab(
        message=callback.message,
        templ=callback_data.templ,
        templates=callback_data.templates,
            )
    await callback.answer()


@router.callback_query(TemplatesCallbackFactory.filter(F.action == "finish"))
async def callbacks_template_finish_fab(callback: CallbackQuery, state: FSMContext):
    """Query with template callback
    # TODO: change me
    """
    user_templ = await state.get_data()
    await state.clear()
    await callback.message.edit_text(f"Your choice: {user_templ.get('template', '-')}")
    await callback.answer()


@router.message(Command('create'))
async def create(
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


@router.message(Command('get'))
async def get(
    message: Message,
    command: CommandObject,
    qm: QuerieMaker
        ) -> None:
    """Get template by name
    # TODO: make humans readable strings
    """
    user_id = message.from_user.id
    if command.args:
        try:
            template = await qm.get_template(user_id, command.args)
            await message.answer(
                f'Query template:'
                f'\nname={template["name"]}'
                    )
        except HttpError as e:
            await message.answer(e.message)
    else:
        await message.answer(
            'Use /get template_name'
            '\n<i>(to get available templates names use /templates)</i>',
            parse_mode="HTML"
                )


@router.message(Command('delete'))
async def delete(
    message: Message,
    command: CommandObject,
    qm: QuerieMaker
        ) -> None:
    """Delete template
    """
    user_id = message.from_user.id
    if command.args:
        try:
            await qm.delete_template(user_id, command.args)
            await message.answer(f'Is deleted template: \n{command.args}')
        except HttpError as e:
            await message.answer(e.message)
    else:
        await message.answer('Use /delete template_name')


async def replace():
    """_summary_
    """
