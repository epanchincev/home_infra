from aiohttp import ClientSession

from app.core.config import settings
from .params import OPEN_DOOR_URL, OPEN_DOOR_BODY, SNAPSHOT_URL

TEMP_DB = {
    1: '26980',
    2: '26981',
    3: '37197',
    4: '36934'
}

async def get_inet_session() -> ClientSession:
    async with ClientSession() as session:
        yield session


class Intercom:
    
    def __init__(self) -> None:
        self._HEADERS = {
            'authorization': settings.authorization,
        }
        
    async def open_door(self, session: ClientSession, door_id: int) -> None:
        async with session.post(
            OPEN_DOOR_URL.format(TEMP_DB[door_id]),
            headers=self._HEADERS,
            json=OPEN_DOOR_BODY
        ) as response:
            response = await response.json()
            print(response['data']['status'])

    
    async def get_image(self, session: ClientSession, door_id: int) -> str:
        async with session.get(
            SNAPSHOT_URL.format(TEMP_DB[door_id]),
            headers=self._HEADERS,
        ) as response:
            return await response.read()

intercom_action = Intercom()
