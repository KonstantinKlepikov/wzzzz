import operator
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Const, Format
from aiogram_dialog.widgets.kbd import Button, Cancel, Multiselect, Url
from aiogram_dialog.widgets.input import MessageInput
from app.schemas.dialog_states import StartGrp, PATTERN
from app.schemas.scheme_errors import HttpError


async def get_expirience(**kwargs):
    """Expirience choices
    # TODO: import and use constraints from api
    """
    expirience = [
        ("no expirience", 'noExperience'),
        ("1-3 ears", 'between1And3'),
        ("3-6 ears", 'between3And6'),
        ("6+ ears", 'moreThan6'),
            ]
    return {
        "expirience": expirience,
            }


async def create_temaplate(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
        ) -> None:
    """Create new template
    """
    user_id = message.from_user.id
    template = dialog_manager.dialog_data["name_input"]
    print(template)
    # TODO: add template fields
    try:
        await dialog_manager.middleware_data["qm"].create_template(user_id, template)
        await message.answer(
            f'Is created template: {dialog_manager.dialog_data["name_input"]}'
                )
        await dialog_manager.switch_to(StartGrp.main)

    except HttpError as e:
        await message.answer(e.message)


# choise expirience and create template
create_template_window = Window(
    Const(
        'Обязательно укажите опыт программирования (используйте пункты меню). '
        'С учетом выбора будет производиться фильтрация '
        'результатов поиска. Вы можете выбрать несколько.'
            ),
    Multiselect(
        Format("✓ {item[0]}"),
        Format("{item[0]}"),
        id="expirience",
        item_id_getter=operator.itemgetter(1),
        items="expirience",
        min_selected=1,
            ),
    Button(Const('создать'), id='create_template', on_click=create_temaplate),
    Url(
        Const("справка по языку запросов"),
        Const("https://hh.ru/article/1175")
            ),
    Cancel(Const('выйти из меню')),
    state=StartGrp.create_template,
    getter=get_expirience
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


define_text = Window(
    Const(
        'Теперь задайте строку запроса (используйте текстовый ввод мессенжера). '
        'Строка запроса используется для фильтрации по текстовому полю и названию вакансий. '
        'К примеру, если задать "game* OR гейм", то будут фильтроваться '
        'вакансии, содержащие в тексте либо в названии одно из указанных слов. '
            ),
    MessageInput(query_text_handler),
    Url(
        Const("справка по языку запросов"),
        Const("https://hh.ru/article/1175")
            ),
    Cancel(Const('выйти из меню')),
    state=StartGrp.define_text,
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
            'Вы пытаетесь использовать недопустимое имя ' \
            'шаблона или шаблон с таким именем уже создан.'
                )


define_name = Window(
    Const(
        'Задайте имя шаблона (используйте текстовый ввод мессенжера). '
        'Не более 20 знаков, Допустимы только ascII буквы, цифры от 0 '
        'до 9 и знак нижнего подчеркивания.'
            ),
    MessageInput(name_handler),
    Url(
        Const("справка по языку запросов"),
        Const("https://hh.ru/article/1175")
            ),
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
                'Сожалеем, но бот не поддерживает больше 10 шаблонов. ' \
                'Удалите или измените один из имеющихся.'
                    )
        else:

            dialog_manager.dialog_data['template_kb_names'] = [n['name'] for n in result['names']]
            await dialog_manager.switch_to(StartGrp.define_name)

    except HttpError as e:
        await c.answer(e.message)
