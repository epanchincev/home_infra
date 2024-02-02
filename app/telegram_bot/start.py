from aiohttp import ClientSession

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import (
    Message, ReplyKeyboardMarkup, InlineKeyboardMarkup,
    CallbackQuery, BufferedInputFile)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from telegram_bot.callback_factory import IntercomCallback
from schemas import IntercomDB
from telegram_bot.local_api import local

router = Router()
router.my_chat_member.filter(F.chat.type == 'private')

INTERCOM_TEXT = '📞Домофоны'
PHOTO_TEXT = '📸Фото'
WELCOME_TEXT = 'Добро пожаловать!'
WELCOME_COMMANDS = ('start', 'keyboard', 'cancel')
TEXT_TAG = {
    INTERCOM_TEXT: 'open',
    PHOTO_TEXT: 'snapshot',
}

def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=INTERCOM_TEXT)
    kb.button(text=PHOTO_TEXT)
    kb.adjust(2)

    return kb.as_markup(resize_keyboard=True)

def get_intercom_keyboard(
    text: str, 
    intercoms: list[IntercomDB],
) -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    tag = TEXT_TAG[text]
    for intercom in intercoms:
        kb.button(
            text=str(intercom),
            callback_data=IntercomCallback(
                action=tag,
                value=intercom.id,
            ),
        )
    kb.adjust(1)
    
    return kb.as_markup()

@router.message(Command(*WELCOME_COMMANDS))
async def cmd_start(
    message: Message,
    **kwargs,
) -> None:
    await message.answer(
        WELCOME_TEXT,
        reply_markup=get_main_keyboard()
    )
    

@router.callback_query(IntercomCallback.filter(F.action == 'open'))
async def open_door(
    callback: CallbackQuery,
    callback_data: IntercomCallback,
    http_session: ClientSession,
    **kwargs,
) -> None:
    opened = await local.open_door(http_session, callback_data.value)
    if opened:
        await callback.answer('Открыто!', show_alert=True)
    else:
        await callback.answer('Ошибка', show_alert=True)


@router.callback_query(IntercomCallback.filter(F.action == 'snapshot'))
async def snapshot(
    callback: CallbackQuery,
    callback_data: IntercomCallback,
    http_session: ClientSession,
    **kwargs,
) -> None:
    photo = await local.get_snapshot(http_session, callback_data.value)
    photo = BufferedInputFile(photo, filename='latest_photo.png')
    await callback.message.answer_photo(photo)
    await callback.answer('ОК')
    
    
@router.message(F.text.in_((INTERCOM_TEXT, PHOTO_TEXT)))
async def get_contorl_keyboard(
    message: Message,
    http_session: ClientSession,
    **kwargs,
) -> None:
    intercoms = await local.get_intercoms(http_session)
    await message.answer(
        message.text,
        reply_markup=get_intercom_keyboard(
            message.text,
            intercoms
        )
    )