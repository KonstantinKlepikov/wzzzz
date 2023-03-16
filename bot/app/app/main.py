import logging
from aiogram import Bot, Dispatcher, executor, types
from app.core.api_queries import QuerieMaker
from app.schemas.scheme_errors import UserNotExistError, UserExistError
from app.config import settings


logging.basicConfig(level=logging.INFO)
bot = Bot(token=settings.API_TOKEN)
dp = Dispatcher(bot)
q = QuerieMaker(bot=bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message) -> None:
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    await message.reply(
        "Hello! \
        \nI'm wzzzz_bot! \
        \nI can help you finde vacancy on hh.ru. \
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

            result = await q.create_user(user_id)
            await message.reply(f"Created user with id={user_id}")

        except UserExistError as e:
            await message.reply(f"{e.message}")


@dp.message_handler()
async def echo(message: types.Message) -> None:

    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
