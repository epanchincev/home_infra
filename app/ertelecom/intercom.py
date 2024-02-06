from datetime import datetime

from aiohttp import ClientSession

from app.core.config import settings
from .params import (
    ACCESSCONTROLS_URL,
    GET_VIDEO_LINK_URL,
    OPEN_DOOR_BODY,
    OPEN_DOOR_URL,
    SNAPSHOT_URL,
)


async def get_inet_session() -> ClientSession:
    async with ClientSession() as session:
        yield session


class Intercom:
    
    def __init__(self) -> None:
        self._HEADERS = {
            'authorization': settings.authorization,
            'Operator': '40',
        }
        self.last_open_time = datetime.now()
        
    async def open_door(self, session: ClientSession, door_id: int) -> None:
        now_time = datetime.now()

        if (now_time - self.last_open_time).seconds < 5:
            return True

        async with session.post(
            OPEN_DOOR_URL.format(door_id),
            headers=self._HEADERS,
            json=OPEN_DOOR_BODY
        ) as response:
            response = await response.json()
            self.last_open_time = now_time
            print(response['data']['status'])

    
    async def get_image(self, session: ClientSession, door_id: int) -> str:
        async with session.get(
            SNAPSHOT_URL.format(door_id),
            headers=self._HEADERS,
        ) as response:
            return await response.read()
        
    async def get_video_link(self, session: ClientSession, door_id: int) -> str | None:
        camera_id = None
        async with session.get(
            ACCESSCONTROLS_URL,
            headers=self._HEADERS,
        ) as response:
            response: dict[str, list] = await response.json()
            for accesscontrol in response['data']:
                if accesscontrol.get('id') == door_id:
                    camera_id = accesscontrol.get('externalCameraId')
                    break
        
        if camera_id:
            async with session.get(
                GET_VIDEO_LINK_URL.format(camera_id),
                headers=self._HEADERS,
            ) as response:
                response = await response.json()

                return response['data']['URL']


intercom_action = Intercom()
