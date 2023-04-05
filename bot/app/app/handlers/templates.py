from typing import Union
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back, Column, Cancel, Url
from aiogram_dialog.widgets.text import Const, Format
from app.schemas.dialog_states import StartGrp, BUTTON_NAMES
from app.schemas.scheme_errors import HttpError
from app.handlers.template import get_template_fields


# buttons for templates kb
buttons = [
    Button(
        Format(f'{{{name}}}'),
        id=name,
        when=f'{name}_extended',
        on_click=get_template_fields
            )
    for name in BUTTON_NAMES
        ]


async def get_templates_buttons(**kwargs) -> dict[str, Union[str, bool]]:
    """Get buttons from db query answer.
    This can be used as colback for temlates Window
    """
    but = kwargs['dialog_manager'].dialog_data['templates_kb_names']
    zipped = zip(BUTTON_NAMES, but)
    button_ex = {f'{name}_extended': False for name in BUTTON_NAMES}
    for name, b in zipped:
        button_ex[name] = "шаблон: "+b
        button_ex[f'{name}_extended'] = True
    return button_ex


templates_window = Window(
    Const('Ваши шаблоны запросов'),
    Column(
        *buttons
    ),
    Url(
        Const("справка по языку запросов"),
        Const("https://hh.ru/article/1175")
            ),
    Back(Const('назад')),
    Cancel(Const('выйти из меню')),
    state=StartGrp.templates,
    getter=get_templates_buttons
        )


async def get_templates_names(
    c: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
        ) -> None:
    """Show available user templates names and add some ui
    """
    user_id = c.from_user.id
    try:
        result = await dialog_manager.middleware_data["qm"].get_templates_names(user_id)
        if result['names']:
            dialog_manager.dialog_data['templates_kb_names'] = [n['name'] for n in result['names']]
            await dialog_manager.switch_to(StartGrp.templates)
        else:
            await c.answer('Ни одного шаблона не найдено. Пожалуйста создайте новый шаблон.')
    except HttpError as e:
        await c.answer(e.message)
