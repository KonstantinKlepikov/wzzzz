import operator
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import Window, DialogManager
from aiogram_dialog.widgets.text import Const, Multi, Format
from aiogram_dialog.widgets.kbd import Button, Cancel, Multiselect
from aiogram_dialog.widgets.input import MessageInput
from app.schemas.dialog_states import StartGrp


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

# choise expirience and create template
create_template_window = Window(
    Multi(
        Const('Finally choose expirience level.'),
        Const('Bla-bla about expirience.'),
        sep='\n'
            ),
    Multiselect(
        Format("✓ {item[0]}"),
        Format("{item[0]}"),
        id="expirience",
        item_id_getter=operator.itemgetter(1),
        items="expirience",
        min_selected=1,
            ),
    Button(Const('create template'), id='create_template'), # TODO: add on_click
    Cancel(Const('exit')),
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
    dialog_manager.dialog_data["name_input"] = message.text
    await dialog_manager.switch_to(StartGrp.create_template)


# query text kb TODO: add back and clear context
define_text = Window(
    Multi(
        Const('Now define query text (use prompt).'),
        Const('Bla-bla how it is.'),
        sep='\n'
            ),
    MessageInput(query_text_handler),
    Cancel(Const('exit')),
    state=StartGrp.define_text,
)


async def name_handler(
    message: Message,
    message_input: MessageInput,
    dialog_manager: DialogManager,
        ) -> None:
    """Define template name
    """
    dialog_manager.dialog_data["text_input"] = message.text
    await dialog_manager.switch_to(StartGrp.define_text)


# Template name kb TODO: back() and clear contaxt
define_name = Window(
    Multi(
        Const('First, define template name (use prompt).'),
        Const('No more than 20 characters, only ascII letters or numbers.'),
        sep='\n'
            ),
    MessageInput(name_handler),
    Cancel(Const('exit')),
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
    # here we check number of templates (no more than 10)
    # TODO: add to api
    await dialog_manager.switch_to(StartGrp.define_name)
