from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import intercom_crud
from app.models import BotUser, Intercom

OBJECT_NOT_FOUND_ERROR = '{} не найден!'
OBJECT_FOUND_ERROR = '{} уже существует!'

def existence_check(object: Intercom | BotUser) -> None:
    """Проверяет существование объекта"""
    if not object:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=OBJECT_NOT_FOUND_ERROR.format(object.__class__.__name__),
        )
        
def not_existence_check(object: Intercom | BotUser) -> None:
    """Проверяет существование объекта"""
    if object:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail=OBJECT_FOUND_ERROR.format(object.__class__.__name__),
        )

async def check_intercom_duplicate(
    intercom_id: int,
    intercom_name: str,
    session: AsyncSession
) -> None:
    intercom_id = await intercom_crud.get_intercom_id_by_name(
        intercom_name, session,
    )
    
    if intercom_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Такое имя домофона уже используется"
        )
        
    intercom_id = await intercom_crud.get_intercom_id_by_intercom_id(
        intercom_id, session,
    )
    
    if intercom_id:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Такой id домофона уже используется"
        )
