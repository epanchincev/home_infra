from aiogram.fsm.state import StatesGroup, State


class BotState(StatesGroup):
    """Состояния в админ режиме."""

    add_photo = State()
