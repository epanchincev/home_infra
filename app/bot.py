import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from core.config import settings
from telegram_bot.start import router
from telegram_bot.middleware import MainMiddleware


file_log = logging.FileHandler('log.txt')
console_out = logging.StreamHandler()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s    %(levelname)s    %(message)s',
    handlers=(file_log, console_out),
)

bot = Bot(settings.bot_token, parse_mode='html')

async def main() -> None:
    dp = Dispatcher(storage=MemoryStorage())
    
    dp.message.outer_middleware(MainMiddleware())
    dp.callback_query.outer_middleware(MainMiddleware())
    
    dp.include_router(router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())