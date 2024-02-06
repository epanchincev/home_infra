import aiohttp
from fastapi import APIRouter, Body, Depends, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import check_intercom_duplicate, existence_check
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud import intercom_crud
from app.ertelecom.intercom import get_inet_session, intercom_action
from app.models import Intercom
from app.schemas import IntercomCreate, IntercomDB, IntercomUpdate

router = APIRouter()

@router.post(
    '/open',
)
async def open_intercom(
    intercom_id: int = Body(...),
    http_session: aiohttp.ClientSession = Depends(get_inet_session),
    session: AsyncSession = Depends(get_async_session),
) -> None:
    intercom_db = await intercom_crud.get(intercom_id, session)
    existence_check(intercom_db)
    await intercom_action.open_door(http_session, intercom_db.intercom_id)


@router.get(
    '/{intercom_id}/snapshot',
)
async def get_snapshot(
    intercom_id: int,
    http_session: aiohttp.ClientSession = Depends(get_inet_session),
    session: AsyncSession = Depends(get_async_session),
) -> Response:
    intercom_db = await intercom_crud.get(intercom_id, session)
    existence_check(intercom_db)
    return Response(
        await intercom_action.get_image(http_session, intercom_db.intercom_id),
        media_type='image/png',
    )


@router.get(
    '/{intercom_id}/videolink',
)
async def get_video_link(
    intercom_id: int,
    http_session: aiohttp.ClientSession = Depends(get_inet_session),
    session: AsyncSession = Depends(get_async_session),
) -> str | None:
    intercom_db = await intercom_crud.get(intercom_id, session)
    existence_check(intercom_db)
    link = await intercom_action.get_video_link(http_session, intercom_db.intercom_id)

    return link


@router.get(
    '/',
    response_model=list[IntercomDB],
)
async def get_all_intercoms(
    session: AsyncSession = Depends(get_async_session),
) -> list[IntercomDB]:
    """Получить все домофоны в БД."""
    return await intercom_crud.get_multi(session)


@router.get(
    '/{intercom_id}',
    response_model=IntercomDB,
)
async def get_intercom(
    intercom_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> IntercomDB:
    """Получить домофон по id"""
    intercom = intercom_crud.get(intercom_id, session)
    existence_check(intercom)
    
    return intercom


@router.post(
    '/',
    response_model=IntercomDB,
    dependencies=[Depends(current_superuser)],
)
async def create_intercom(
    intercom: IntercomCreate,
    session: AsyncSession = Depends(get_async_session),
) -> IntercomDB:
    """
    Только для суперюзеров.\n
    Создать новый домофон"""
    await check_intercom_duplicate(
        intercom.intercom_id,
        intercom.name,
        session,
    )
    new_intercom = Intercom(**intercom.model_dump())
    session.add(new_intercom)
    await session.commit()
    await session.refresh(new_intercom)
    
    return new_intercom


@router.delete(
    '/{intercom_id}',
    response_model=IntercomDB,
    dependencies=[Depends(current_superuser)],
)
async def delete_intercom(
    intercom_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> IntercomDB:
    """
    Только для суперюзеров.\n
    Удаляет домофон.
    """
    project = await intercom_crud.get(intercom_id, session)
    existence_check(project)
    project = await intercom_crud.remove(project, session)

    return project

@router.patch(
    '/{intercom_id}',
    response_model=IntercomDB,
    dependencies=[Depends(current_superuser)],
)
async def update_intercom(
    intercom_id: int,
    intercom_in: IntercomUpdate,
    session: AsyncSession = Depends(get_async_session),
) -> IntercomDB:
    """
    Только для суперюзеров.\n
    Редактирование домофона.
    """
    intercom = await intercom_crud.get(intercom_id, session)

    existence_check(intercom)

    check_intercom_duplicate(
        intercom_in.intercom_id, 
        intercom_in.name, 
        session,
    )

    intercom = await intercom_crud.update(
        intercom, intercom_in, session,
    )

    return intercom
