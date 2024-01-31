import aiohttp
from fastapi import APIRouter, Depends, Response, Body

from app.ertelecom.intercom import intercom, get_inet_session

router = APIRouter()

@router.post(
    '/open',
)
async def open_intercom(
    intercom_id: int = Body(...),
    http_session: aiohttp.ClientSession = Depends(get_inet_session),
) -> None:
    await intercom.open_door(http_session, intercom_id)


@router.get(
    '/snapshot/{intercom_id}',
)
async def get_snapshot(
    intercom_id: int,
    http_session: aiohttp.ClientSession = Depends(get_inet_session),
) -> Response:
    return Response(
        await intercom.get_image(http_session, intercom_id),
        media_type='image/png',
    )
