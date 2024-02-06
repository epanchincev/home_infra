import asyncio
from http import HTTPStatus

from aiohttp import ClientSession

from core.config import settings
from schemas import FaceRecognitionRead, IntercomDB


class LocalAPI:
    
    _HEADER = {
        'Authorization': None
    }
    _AUTH_DATA = {
        'username': settings.bot_email,
        'password': settings.bot_password,
    }
    _BASE_URL = f'http://{settings.api_url}'
    _AUTH_URL = f'{_BASE_URL}/auth/jwt/login'
    _INTERCOM_URL = f'{_BASE_URL}/intercom'
    _BOT_USER_URL = f'{_BASE_URL}/bot_user'
    _RECOGNITION_URL = f'{_BASE_URL}/recognition/'
    
    def __init__(self) -> None:
        asyncio.run(self.get_api_token())
    
    async def get_api_token(self) -> None:
        async with ClientSession() as session:
            async with session.post(
                self._AUTH_URL,
                data=self._AUTH_DATA
            ) as response:
                response = await response.json()
                self._HEADER['Authorization'] = f'Bearer {response["access_token"]}'
                
                
    async def open_door(self, session: ClientSession, door_id: int) -> bool:
        async with session.post(
            self._INTERCOM_URL + '/open',
            json=str(door_id),
            headers=self._HEADER,
        ) as response:
                return response.status == HTTPStatus.OK
            
    async def get_snapshot(self, session: ClientSession, door_id: int) -> bytes:
        async with session.get(
            f'{self._INTERCOM_URL}/snapshot/{door_id}',
            headers=self._HEADER
        ) as response:
            return await response.read()
        
    async def bot_user_exist(self, session: ClientSession, bot_user_id:int) -> bool:
        async with session.get(
            f'{self._BOT_USER_URL}/{bot_user_id}',
            headers=self._HEADER,
        ) as response:
            return response.status == HTTPStatus.OK
        
    async def get_intercoms(self, session: ClientSession) -> list[IntercomDB]:
        async with session.get(
            self._INTERCOM_URL,
            headers=self._HEADER,
        ) as response:
            response = await response.json()
            
            return [IntercomDB(**answer) for answer in response]
        
    async def add_face_to_recognition(
        self,
        session: ClientSession,
        image: bytes,
        name: str,
        from_id: int | None = None,
    ) -> FaceRecognitionRead:
        async with session.post(
            self._RECOGNITION_URL,
            headers=self._HEADER,
            data={
                'image': image,
                'name': name,
                'from_id': str(from_id),
            }
        ) as response:
            response = await response.json()
            
            return FaceRecognitionRead(**response)


local = LocalAPI()

