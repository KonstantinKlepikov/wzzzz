import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from app.core.api_queries import QuerieMaker
from app.schemas.scheme_errors import HttpError
from app.config import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher(bot)
q = QuerieMaker(bot)


@dp.message_handler(commands=['start',])
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
        "Hello! \
        \nI'm wzzzz_bot! \
        \nI can help you find vacancy on hh.ru. \
        \n\nCommands: \
        \n/templates \
        \n/create"
            )


@dp.message_handler(commands=['templates',])
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


@dp.message_handler(commands=['create',])
async def create_template(message: Message) -> None:
    """Create new clear template with given name
    """


@dp.message_handler()
async def echo(message: Message) -> None:

    await message.reply(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
