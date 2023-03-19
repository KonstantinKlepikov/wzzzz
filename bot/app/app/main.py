import logging
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
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
        await message.answer(f'Your id: {result["user_id"]}')

    except HttpError as e:
        await message.answer(e.message)

        try:
            await q.create_user(user_id)
            await message.answer(f"You registred with id: {user_id}")
        except HttpError as e:
            await message.answer(e.message)

    await message.answer(
        "<b>Hello</b> \
        \nI'm wzzzz_bot \
        \nI can help you find vacancy on hh.ru \
        \n\nCommands: \
        \n- /templates \
        \n- /create <i>template_name</i> \
        \n  (no more than 20 characters, only ascII letters or numbers)",
        parse_mode="HTML"
            )


@dp.message(Command('templates'))
async def get_templates(message: Message) -> None:
    """Show user templates names
    """
    user_id = message.from_user.id
    try:
        result = await q.get_templates_names(user_id)
        names = '\n'.join(name['name'] for name in result['names'])
        temp = names if names else 'no templates found.'
        await message.answer(f'Your templates: \n{temp}')
    except HttpError as e:
        await message.answer(e.message)


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
            'Use /create <i>template_name</i> \
            \n(no more than 20 characters, only ascII letters or numbers)',
            parse_mode="HTML"
                )


async def main():
    """Start bot"""
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    asyncio.run(main())
