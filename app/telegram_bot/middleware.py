from typing import Any, Awaitable, Callable, Dict
import logging

from aiohttp import ClientSession
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.exceptions import TelegramBadRequest

from api_client.local_api import local


class MainMiddleware(BaseMiddleware):
    
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        async with ClientSession() as http_session:
            user = await local.bot_user_exist(http_session, event.from_user.id)
            
            if not user:
                await event.answer('Закрыто')
                return

            data['http_session'] = http_session
            try:
                await handler(event, data)
            except TelegramBadRequest:
                await event.answer('Ошибка!')
                logging.error(
                    f'{user.tg_id} Ошибка при запросе: "{event.text}"'
                )
        return await super().__call__(handler, event, data)
