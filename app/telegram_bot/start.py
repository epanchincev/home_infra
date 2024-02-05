from aiohttp import ClientSession
from aiogram import F, Router, Bot
from aiogram.filters import Command, StateFilter
from aiogram.types import (
    Message, ReplyKeyboardMarkup, InlineKeyboardMarkup,
    CallbackQuery, BufferedInputFile)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from telegram_bot.states import BotState
from telegram_bot.callback_factory import IntercomCallback
from schemas import IntercomDB
from api_client.local_api import local

router = Router()
router.my_chat_member.filter(F.chat.type == 'private')

INTERCOM_TEXT = '📞Домофоны'
PHOTO_TEXT = '📸Фото в распознавание'
WELCOME_TEXT = 'Добро пожаловать!'
WELCOME_COMMANDS = ('start', 'keyboard', 'cancel')
TEXT_TAG = {
    INTERCOM_TEXT: 'open',
    PHOTO_TEXT: 'snapshot',
}
TEXT_SET_STATE_ADD_PHOTO = (
    'Отправьте фото гостя и подпишите его имя в одном сообщении.'
    'На фото должно быть одно лицо.'
)
BACK_TO_MENU = '↩️В главное меню'

def get_back_to_menu_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text=BACK_TO_MENU)

    return kb.as_markup(resize_keyboard=True)


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
    state: FSMContext,
    **kwargs,
) -> None:
    await state.clear()
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
    
    
@router.message(F.text == INTERCOM_TEXT)
async def get_control_keyboard(
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
    
@router.message(F.text == PHOTO_TEXT)
async def set_state_add_photo_to_known_faces(
    message: Message,
    state: FSMContext,
) -> None:
    await state.set_state(BotState.add_photo)
    await message.answer(
        TEXT_SET_STATE_ADD_PHOTO,
        reply_markup=get_back_to_menu_keyboard(),
    )
    
@router.message(F.text == BACK_TO_MENU)
async def back_to_menu(
    message: Message,
    state: FSMContext,
    bot
) -> None:
    await state.clear()
    await message.answer(
        'Главное меню',
        reply_markup=get_main_keyboard(),
    )

@router.message(StateFilter(BotState.add_photo))
async def add_photo_to_known_faces(
    message: Message,
    http_session: ClientSession,
    bot: Bot,
) -> None:
    photos = message.photo
    
    if not photos:
        await message.answer('Фото не отправлено.')
        return

    if not message.caption:
        await message.answer('Отсутвует имя')
        return
    
    photo = photos.pop()
    file = await bot.get_file(photo.file_id)
    photo = await bot.download_file(file.file_path)
    
    face = await local.add_face_to_recognition(
        http_session, photo, message.caption, message.from_user.id,
    )
    
    await message.answer(f'Создан объект: {face}')
