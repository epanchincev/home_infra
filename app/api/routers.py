from fastapi import APIRouter

from app.api.endpoints import user_router, intercom_router, bot_user_router

main_router = APIRouter()
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
