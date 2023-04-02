from aiogram.fsm.state import State, StatesGroup


class StartGrp(StatesGroup):
    main = State()
    templates = State()
    template = State()
    define_name = State()
    define_text = State()
    create_template = State()


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
