import asyncio
from redis.asyncio import Redis
from aiogram.types import CallbackQuery
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.kbd import Button, Back, Column, Cancel
from aiogram_dialog.widgets.text import Const, Format
from app.db.init_redis import RedisConnection
from app.schemas.dialog_states import StartGrp, BUTTON_NAMES, QUERY_INFO
from app.schemas.scheme_errors import HttpError


async def query_with_template(
    c: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
        ) -> None:
    """Query vacancies
    """
    user_id = c.from_user.id
    template = dialog_manager.dialog_data.get('template')
    if template:
        async with RedisConnection() as redis_db:
            async with redis_db.pubsub() as pubsub:
                await pubsub.subscribe(str(user_id))
                try:
                    await dialog_manager.middleware_data["qm"].get_vacancies(
                        user_id, template['name']
                            )
                    await c.answer(
                        'Запрошены новые вакансии. Пришлем csv после обработки запроса.'
                            )
                    while True:
                        message = await pubsub.get_message(ignore_subscribe_messages=True)
                        if message:
                            print(message)  # TODO: get csv
                            break
                        await asyncio.sleep(0.001)  # TODO: make exit if to long request
                except HttpError as e:
                    await c.answer(e.message)
    else:
        c.answer('Шаблон с таким именем не существует.')


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
            await dialog_manager.middleware_data["qm"].delete_template(
                user_id, template['name']
                    )
            await c.answer(f'Удален шаблон с именем: {template["name"]}')
            await dialog_manager.switch_to(StartGrp.main)
        except HttpError as e:
            await c.answer(e.message)
    else:
        c.answer('Шаблон с таким именем не существует.')


async def get_template_fields(**kwargs) -> str:
    """Get template fields
    """
    template = kwargs['dialog_manager'].dialog_data['template']
    result = 'Поля шаблона:' \
             f'\nимя: {template.get("name") or "-"}' \
             f'\nопыт: {template.get("expirience") or "-"}' \
             f'\nтекст запроса: {template.get("text") or "-"}' \
             '\n\nВ дополнение к этому ищутся вакансии:' \
             '\n- только для удаленной работы' \
             '\n- не старше 2-х месяцев от текущей даты'\
             '\n- доступные в России, Казахстане и Грузии' \
             '\n- с полной или частичной занятостью' \
             '\n- программисты, тестировщики, девопсы и датасаентисты'

    return {'text': result}


# display template fields and query dialogue
template_window = Window(
    Format('{text}'),
    Column(
        Button(
            Const('запросить вакансии'),
            id='query_for_vacancies',
            on_click=query_with_template
                ),
        Button(
            Const('изменить поля шаблона (не реализовано)'),
            id='change_template_fields'
                ),  # TODO:
        Button(
            Const('удалить шаблон'),
            id='delete_template',
            on_click=delete_template
                ),
            ),
    QUERY_INFO,
    Back(Const('назад')),
    Cancel(Const('выйти из меню')),
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
            dialog_manager.dialog_data['templates_kb_names'][
                BUTTON_NAMES.index(button.widget_id)
                    ]
                )
        dialog_manager.dialog_data['template'] = template
        await dialog_manager.switch_to(StartGrp.template)

    except HttpError as e:
        await c.answer(e.message)
