from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import Window, Dialog, DialogRegistry, DialogManager, StartMode
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button


class StartGrp(StatesGroup):
    start = State()


start_window = Window(
    Const("Hello, unknown person"),
    Button(Const("Say nothing"), id="nothing"),
    state=StartGrp.start,
        )


start_dialogue = Dialog(start_window)
