from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back, Column, Cancel
from aiogram_dialog.widgets.text import Const, Format
from app.schemas.dialog_states import StartGrp, button_names
from app.schemas.scheme_errors import HttpError


async def delete_template(
    c: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
        ) -> None:
    """Delete template
    """
    user_id = c.from_user.id
    template = dialog_manager.dialog_data.get('template')
    if template:
        try:
            await dialog_manager.middleware_data["qm"].delete_template(user_id, template['name'])
            await c.answer(f'Is deleted template: {template["name"]}')
        except HttpError as e:
            await c.answer(e.message)
    else:
        c.answer(f'You must choose template to delete.')


async def get_template_fields(**kwargs) -> str:
    """Get template fields
    """
    template = kwargs['dialog_manager'].dialog_data['template']
    result = 'Template fields' \
            f'\nname: {template.get("name") or "-"}' \
            f'\nexpirience: {template.get("expirience") or "-"}' \
            f'\ntext: {template.get("text") or "-"}'
    return {'text': result}


# display template fields and query dialogue
template_window = Window(
    Format('{text}'),
    Column(
        Button(Const('query for vacancies'), id='query_for_vacancies'),
        Button(Const('change template fields'), id='change_template_fields'),
        Button(Const('delete template'), id='delete_template', on_click=delete_template),
            ),
    Back(Const('back to list of templates')),
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