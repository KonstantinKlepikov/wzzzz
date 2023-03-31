from typing import Union
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back, Column, Cancel
from aiogram_dialog.widgets.text import Const, Format
from app.schemas.dialog_states import StartGrp
from app.schemas.scheme_errors import HttpError


# button ids for templates kb
button_names = [
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten'
        ]

async def get_template_fields(**kwargs) -> str:
    """Get template fields
    """
    template = kwargs['dialog_manager'].dialog_data['template']
    result = 'Template fields' \
            f'\nname: {template.get("name", "-")}' \
            f'\nexpirience: {template.get("expirience", "-")}' \
            f'\ntext: {template.get("text", "-")}'
    return {'text': result}


# display template fields and query dialogue
template_window = Window(
    Format('{text}'),
    Column(
        Button(Const('query for vacancies'), id='query_for_vacancies'),
        Button(Const('change template fields'), id='change_template_fields'),
        Button(Const('delete templates'), id='delete_template'),
            ),
    Back(Const('back to templates')),
    Cancel(Const('exit')),
    state=StartGrp.template,
    getter=get_template_fields
        )


async def get_template_fields(
    c: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
        ) -> None:
    """Display template fields
    """
    user_id = c.from_user.id
    try:
        template = await dialog_manager.middleware_data["qm"].get_template(
            user_id,
            dialog_manager.dialog_data['names'][button_names.index(button.widget_id)]['name']
                )
        dialog_manager.dialog_data['template'] = template
        await dialog_manager.switch_to(StartGrp.template)

    except HttpError as e:
        await c.answer(e.message)


# buttons for templates kb
buttons = [
    Button(
        Format(f'{{{name}}}'),
        id=name,
        when=f'{name}_extended',
        on_click=get_template_fields
            )
    for name in button_names
        ]


async def get_templates_buttons(**kwargs) -> dict[str, Union[str, bool]]:
    """Get buttons from db query answer.
    This can be used as colback for temlates Window
    """
    but = [n['name'] for n in kwargs['dialog_manager'].dialog_data['names']]
    zipped = zip(button_names, but)
    button_ex = {f'{name}_extended': False for name in button_names}
    for name, b in zipped:
        button_ex[name] = b
        button_ex[f'{name}_extended'] = True
    return button_ex


templates_window = Window(
    Const('Awailable templates'),
    Column(
        *buttons
    ),
    Back(Const('back to main menu')),
    Cancel(Const('exit')),
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
            dialog_manager.dialog_data['names'] = result['names']
            await dialog_manager.switch_to(StartGrp.templates)
        else:
            await c.answer('Templates not found. Pls, create new.')
    except HttpError as e:
        await c.answer(e.message)
