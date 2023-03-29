from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from app.schemas.scheme_errors import HttpError
from app.middleware.api_queries import QuerieMaker
from app.keyboards.start import StartGrp


router = Router()


@router.message(Command('start'))
async def start_work(
    message: Message,
    qm: QuerieMaker,
    dialog_manager: DialogManager
        ) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    await dialog_manager.start(StartGrp.start, mode=StartMode.RESET_STACK)

    user_id = message.from_user.id
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
        '\nCreate and use query templates to get vacancies in .csv format'
        '\n\nCommands:'
        '\n- /templates'
        ' <i>(get list of available templates)</i>'
        '\n- /get_vacancies'
        ' <i>(request vacancies with query template)</i>'
        '\n- /create template_name'
        ' <i>(no more than 20 characters, only ascII letters or numbers)</i>'
        '\n- /get template_name'
        ' <i>(rget query parameters of template)</i>'
        '\n- /delete template_name'
        ' <i>(delete template)</i>',
        parse_mode="HTML"
            )
