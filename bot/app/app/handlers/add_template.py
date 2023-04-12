import operator
from typing import Any
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager, ChatEvent
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import (
    Button,
    Cancel,
    Multiselect,
    Select,
    ManagedMultiSelectAdapter,
        )
from aiogram_dialog.widgets.input import MessageInput
from app.schemas.dialog_states import StartGrp, PATTERN, QUERY_INFO
from app.schemas.scheme_errors import HttpError


async def get_buttons(**kwargs):
    """Expirience choices
    # TODO: import and use constraints from api
    """
    expirience = [
        ("no expirience", 'noExperience'),
        ("1-3 ears", 'between1And3'),
        ("3-6 ears", 'between3And6'),
        ("6+ ears", 'moreThan6'),
            ]
    q = [
        ("ищем питониста", 'python* OR Python* OR питон OR python'),
        ("ищем разработчика игр", 'game* OR Game* OR гейм OR Гейм*'),
            ]
    return {
        "expirience": expirience,
        "text_q": q,
            }


async def multiselect_changed(
    event: ChatEvent,
    select: ManagedMultiSelectAdapter,
    dialog_manager: DialogManager,
    *args,
    **kwargs
        ) -> None:
    dialog_manager.dialog_data["expirience_input"] = select.get_checked()


async def create_temaplate(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
        ) -> None:
    """Create new template
    """
    user_id = message.from_user.id
    template = dialog_manager.dialog_data["name_input"]
    params = {
        "name": template,
        "expirience": dialog_manager.dialog_data["expirience_input"],
        "text": dialog_manager.dialog_data["text_input"],
            }
    try:
        await dialog_manager.middleware_data["qm"].create_template(user_id, template)
        await dialog_manager.middleware_data["qm"].replace_template(user_id, params)
        await message.answer(
            f'Is created template: {dialog_manager.dialog_data["name_input"]}'
                )
        await dialog_manager.switch_to(StartGrp.main)

    except HttpError as e:
        await message.answer(e.message)


# choose expirience and create template
create_template_window = Window(
    Const(
        'Обязательно укажите опыт программирования (используйте пункты меню). '
        'С учетом выбора будет производиться фильтрация '
        'результатов поиска. Вы можете выбрать несколько.'
            ),
    Multiselect(
        Format("✓ {item[0]}"),
        Format("{item[0]}"),
        id="expirience_input",
        item_id_getter=operator.itemgetter(1),
        items="expirience",
        min_selected=1,
        on_state_changed=multiselect_changed
            ),
    Button(Const('создать шаблон'), id='create_template', on_click=create_temaplate),
    Cancel(Const('выйти из меню')),
    state=StartGrp.create_template,
    getter=get_buttons
        )


async def query_text_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
        ) -> None:
    """Define query text
    """
    if message.text:
        dialog_manager.dialog_data["text_input"] = message.text
        await dialog_manager.switch_to(StartGrp.create_template)
    else:
        await message.reply('Вы используете недопустимую строку запроса.')


async def query_text_calback(
    c: CallbackQuery,
    widget: Any,
    dialog_manager: DialogManager,
    item_id: str
        ) -> None:
    """Define query text
    """
    dialog_manager.dialog_data["text_input"] = item_id
    await dialog_manager.switch_to(StartGrp.create_template)


define_text = Window(
    Const(
        'Теперь задайте строку запроса '
        '(используйте текстовый ввод мессенжера или выберите из списка). '
        'Строка запроса используется для фильтрации по текстовому '
        'полю и названию вакансий. '
        'К примеру, если задать "game* OR гейм", то будут отфильтрованы '
        'вакансии, содержащие в тексте/названии одно из указанных слов. '
            ),
    Select(
        Format("{item[0]}"),
        id="text_query",
        item_id_getter=operator.itemgetter(1),
        items="text_q",
        on_click=query_text_calback
            ),
    MessageInput(query_text_handler),
    QUERY_INFO,
    Cancel(Const('выйти из меню')),
    state=StartGrp.define_text,
    getter=get_buttons
)


async def name_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
        ) -> None:
    """Define template name
    """
    if PATTERN.match(message.text) \
            and len(message.text) <= 20 \
            and message.text not in dialog_manager.dialog_data['template_kb_names']:
        dialog_manager.dialog_data["name_input"] = message.text
        await dialog_manager.switch_to(StartGrp.define_text)
    else:
        await message.reply(
            'Вы пытаетесь использовать недопустимое имя '
            'шаблона или шаблон с таким именем уже создан.'
                )


define_name = Window(
    Const(
        'Задайте имя шаблона (используйте текстовый ввод мессенжера). '
        'Не более 20 знаков, Допустимы только ascII буквы, цифры от 0 '
        'до 9 и знак нижнего подчеркивания.'
            ),
    MessageInput(name_handler),
    Cancel(Const('выйти из меню')),
    state=StartGrp.define_name,
        )


async def create_new_template(
    c: CallbackQuery,
    button: Button,
    dialog_manager: DialogManager
        ) -> None:
    """Create new template with given name
    """
    user_id = c.from_user.id
    try:
        result = await dialog_manager.middleware_data["qm"].get_templates_names(user_id)
        if result['names'] and len(result['names']) > 10:

            await c.answer(
                'Сожалеем, но бот не поддерживает больше 10 шаблонов. '
                'Удалите или измените один из имеющихся.'
                    )
        else:

            dialog_manager.dialog_data['template_kb_names'] = [
                n['name'] for n in result['names']
                    ]
            await dialog_manager.switch_to(StartGrp.define_name)

    except HttpError as e:
        await c.answer(e.message)
