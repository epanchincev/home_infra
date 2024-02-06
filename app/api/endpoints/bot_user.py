from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import existence_check, not_existence_check
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import bot_user_crud
from app.models import BotUser
from app.schemas import BotUserCreate, BotUserDB, BotUserUpdate

router = APIRouter()


@router.get(
    '/',
    response_model=list[BotUserDB],
)
async def get_all_bot_users(
    session: AsyncSession = Depends(get_async_session),
) -> list[BotUserDB]:
    """Получить всех пользователей бота в БД."""
    return await bot_user_crud.get_multi(session)


@router.get(
    '/{bot_user_id}',
    response_model=BotUserDB,
)
async def get_bot_user(
    bot_user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> BotUserDB:
    """Получить пользователя бота по id"""
    bot_user = await bot_user_crud.get(bot_user_id, session)
    existence_check(bot_user)
    
    return bot_user


@router.post(
    '/',
    response_model=BotUserDB,
    dependencies=[Depends(current_superuser)],
)
async def create_bot_user(
    bot_user: BotUserCreate,
    session: AsyncSession = Depends(get_async_session),
) -> BotUserDB:
    """
    Только для суперюзеров.\n
    Создать нового пользователя бота"""
    exist_bot_user = await bot_user_crud.get(bot_user.id)
    not_existence_check(exist_bot_user)
    new_bot_user = BotUser(**bot_user.model_dump())
    session.add(new_bot_user)
    await session.commit()
    await session.refresh(new_bot_user)
    
    return new_bot_user


@router.delete(
    '/{bot_user_id}',
    response_model=BotUserDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_bot_user(
    bot_user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> BotUserDB:
    """
    Только для суперюзеров.\n
    Удаляет пользователя бота.
    """
    bot_user = await bot_user_crud.get(bot_user_id, session)
    existence_check(bot_user)
    bot_user = await bot_user_crud.remove(bot_user, session)

    return bot_user

@router.patch(
    '/{bot_user_id}',
    response_model=BotUserDB,
    dependencies=[Depends(current_superuser)],
)
async def update_bot_user(
    bot_user_id: int,
    bot_user_in: BotUserUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> BotUserDB:
    """
    Только для суперюзеров.\n
    Редактирование пользователя бота.
    """
    bot_user = await bot_user_crud.get(bot_user_id, session)

    existence_check(bot_user)

    bot_user = await bot_user_crud.update(
        bot_user, bot_user_in, session,
    )

    return bot_user
