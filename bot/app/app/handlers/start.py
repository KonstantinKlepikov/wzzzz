from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.schemas.scheme_errors import HttpError
from app.middleware.api_queries import QuerieMaker


router = Router()


@router.message(Command('start'))
async def start_work(message: Message, qm: QuerieMaker) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    user_id = message.from_user.id
    print(qm)
    try:
        result = await qm.get_user(user_id)
        await message.answer(f'Your login with id: {result["user_id"]}')

    except HttpError as e:
        await message.answer(e.message)

        try:
            await qm.create_user(user_id)
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
