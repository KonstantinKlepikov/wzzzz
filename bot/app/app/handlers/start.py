from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, Window
from aiogram_dialog.widgets.text import Multi, Const
from aiogram_dialog.widgets.kbd import Button, Column, Cancel
from app.schemas.scheme_errors import HttpError
from app.schemas.dialog_states import StartGrp
from app.middleware.api_queries import QuerieMaker
from app.handlers.templates import get_templates_names
from app.handlers.add_template import create_new_template


router = Router()


start_window = Window(
    Multi(
        Const('wzzzz помогает искать вакансии программиста на hh.ru'),
        Const('Создавайте шаблоны запроса и используйте их для поиска.'),
        sep='\n'
            ),
    Column(
        Button(
            Const("мои шаблоны"),
            id="all_templates",
            on_click=get_templates_names
                ),
        Button(
            Const("создать новый шаблон"),
            id="create_new_template",
            on_click=create_new_template
                ),
            ),
    Cancel(Const('выйти из меню')),
    state=StartGrp.main,
        )


@router.message(Command('start'))
async def start_work(
    message: Message,
    qm: QuerieMaker,
    dialog_manager: DialogManager
        ) -> None:
    """
    This handler will be called when user sends `/start` command
    """
    user_id = message.from_user.id
    try:
        await qm.get_user(user_id)
        # result = await qm.get_user(user_id)
        # await message.answer(f'Your login with id: {result["user_id"]}')
        await dialog_manager.start(StartGrp.main, mode=StartMode.RESET_STACK)

    except HttpError as e:
        # await message.answer(e.message)

        try:
            await qm.create_user(user_id)
            # await message.answer(f"You registred and login with id: {user_id}")
            await dialog_manager.start(StartGrp.main, mode=StartMode.RESET_STACK)
        except HttpError as e:
            await message.answer(e.message)
