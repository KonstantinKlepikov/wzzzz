import re
from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Url


class StartGrp(StatesGroup):
    main = State()
    templates = State()
    template = State()
    define_name = State()
    define_text = State()
    create_template = State()


# button ids for templates kb
BUTTON_NAMES = [
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
PATTERN = re.compile('^[A-Za-z0-9_-]*$')
QUERY_INFO = Url(
    Const("справка по языку запросов"),
    Const("https://hh.ru/article/1175")
        )
