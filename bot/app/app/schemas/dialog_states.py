import re
from aiogram.fsm.state import State, StatesGroup


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
