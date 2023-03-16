import os
import logging
from aiogram import Bot, Dispatcher, executor, types


API_TOKEN = os.environ['API_TOKEN']


# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


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

    await message.answer(
        f'Я идентифицировал тебя как {message.from_user.username} с id={message.from_user.id}'
        )


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
