import logging
import asyncio
from contextlib import suppress
from typing import Optional
from magic_filter import F
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command, CommandObject
from aiogram.exceptions import TelegramBadRequest
from app.core.api_queries import QuerieMaker
from app.schemas.scheme_errors import HttpError
from app.config import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.API_TOKEN.get_secret_value())
dp = Dispatcher()
q = QuerieMaker(bot)


@dp.message(Command('start'))
async def start_work(message: Message) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    user_id = message.from_user.id
    try:
        result = await q.get_user(user_id)
        await message.answer(f'Your login with id: {result["user_id"]}')

    except HttpError as e:
        await message.answer(e.message)

        try:
            await q.create_user(user_id)
            await message.answer(f"You registred and login with id: {user_id}")
        except HttpError as e:
            await message.answer(e.message)

    await message.answer(
        '<b>Hello!</b> This bot help you find vacancy on hh.ru'
        '\n Create and use searchig templates to get vacancies in csv format'
        '\n\nCommands:'
        '\n- /get_vacancies'
        ' <i>(request vacancies with query template)</i>'
        '\n- /create template_name'
        ' <i>(no more than 20 characters, only ascII letters or numbers)</i>',
        parse_mode="HTML"
            )

user_data = {}


class TemplatesCallbackFactory(CallbackData, prefix="templ"):
    action: str
    templates: str
    templ: Optional[str]


def get_templates_keyboard_fab(templates: str):
    builder = InlineKeyboardBuilder()
    for t in templates.split('|'):
        builder.button(
            text=t,
            callback_data=TemplatesCallbackFactory(
                action="change",
                templates=templates,
                templ=t
                    )
                )
    builder.button(
        text='👌 query for vacancies',
        callback_data=TemplatesCallbackFactory(
            action="finish",
            templates=templates,
                )
            )
    builder.adjust(3)
    return builder.as_markup()


async def update_choice_text_fab(message: Message, templ: str, templates: str):
    with suppress(TelegramBadRequest):
        await message.edit_text(
            f"Choose template for query: {templ}",
            reply_markup=get_templates_keyboard_fab(templates)
                )


@dp.message(Command('get_vacancies'))
async def get_vacancies(message: Message) -> None:
    """Show user templates names
    """
    user_id = message.from_user.id
    user_data[user_id] = '-'
    try:
        result = await q.get_templates_names(user_id)
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


@dp.callback_query(TemplatesCallbackFactory.filter(F.action == "change"))
async def callbacks_template_change_fab(
    callback: CallbackQuery,
    callback_data: TemplatesCallbackFactory
        ):
    user_id = callback.from_user.id

    user_data[user_id] = callback_data.templ
    await update_choice_text_fab(
        message=callback.message,
        templ=callback_data.templ,
        templates=callback_data.templates,
            )
    await callback.answer()


@dp.callback_query(TemplatesCallbackFactory.filter(F.action == "finish"))
async def callbacks_template_finish_fab(callback: CallbackQuery):
    user_templ = user_data.get(callback.from_user.id, '-')

    await callback.message.edit_text(f"Your choice: {user_templ}")
    await callback.answer()


@dp.message(Command('create'))
async def create_template(message: Message, command: CommandObject) -> None:
    """Create new clear template with given name
    """
    user_id = message.from_user.id
    if command.args:
        try:
            await q.create_template(user_id, command.args)
            await message.answer(f'Is created template: \n{command.args}')
        except HttpError as e:
            await message.answer(e.message)
    else:
        await message.answer(
            'Use /create template_name \
            \n<i>(no more than 20 characters, only ascII letters or numbers)</i>',
            parse_mode="HTML"
                )


async def main():
    """Start bot"""
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
