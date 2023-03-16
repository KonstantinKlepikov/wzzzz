import logging
from aiogram import Bot, Dispatcher, executor, types
from app.core.api_queries import QuerieMaker
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
        "Привет! \
        \nЯ wzzzz_bot! \
        \nЯ помогу тебе подыскать вакансии на hh.ru. \
        \nПока что я ничего не умею, но скоро научусь. \
        \nПопробуй поговорить со мной."
        )


@dp.message_handler()
async def echo(message: types.Message) -> None:

    result = await q.get_user(user_id=message.from_user.id)

    await message.answer(
        f'Я идентифицировал тебя как {message.from_user.username} \
        \nс id={message.from_user.id}. \
        \nApi answers: {result["detail"]}'
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
