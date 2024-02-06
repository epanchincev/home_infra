from fastapi import APIRouter

from app.api.endpoints import (bot_user_router, intercom_router,
                               recognition_router, user_router)

main_router = APIRouter(prefix='/api/v1')
main_router.include_router(user_router)
main_router.include_router(
    intercom_router,
    prefix='/intercom',
    tags=['Домофон'],
)
main_router.include_router(
    bot_user_router,
    prefix='/bot_user',
    tags=['Пользователи бота']
)
main_router.include_router(
    recognition_router,
    prefix='/recognition',
    tags=['Распознавание лиц']
)
