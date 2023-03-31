from aiogram.fsm.state import State, StatesGroup


class StartGrp(StatesGroup):
    main = State()
    templates = State()
    template = State()
