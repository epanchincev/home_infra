from aiogram.fsm.state import State, StatesGroup


class BotState(StatesGroup):
    """Состояния в админ режиме."""

    add_photo = State()
