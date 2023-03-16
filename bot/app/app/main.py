import logging
from aiogram import Bot, Dispatcher, executor
from aiogram.types import Message
from app.core.api_queries import QuerieMaker
from app.schemas.scheme_errors import UserNotExistError, UserExistError
from app.config import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher(bot)
q = QuerieMaker(bot)


@dp.message_handler(commands=['start',])
async def send_welcome(message: Message) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    await message.reply(
        "Hello! \
        \nI'm wzzzz_bot! \
        \nI can help you find vacancy on hh.ru. \
        \nTalk with me."
        )

    user_id = message.from_user.id

    try:

        result = await q.get_user(user_id)
        await message.reply(
            f'You are {message.from_user.username} \
            \nId in db: id={result["user_id"]}'
                )

    except UserNotExistError as e:
        await message.reply(f"{e.message}")

        try:

            await q.create_user(user_id)
            await message.reply(f"Created user with id={user_id}")

        except UserExistError as e:
            await message.reply(f"{e.message}")


@dp.message_handler()
async def echo(message: Message) -> None:

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
