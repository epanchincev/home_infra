from aiogram.filters.callback_data import CallbackData


class IntercomCallback(CallbackData, prefix='intercom'):
    action: str
    value: int
