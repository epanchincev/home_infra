from .base import CRUDBase
from app.models import BotUser


class CRUDBotUser(CRUDBase):
    """CRUD для пользователей бота"""
    
    pass


bot_user_crud = CRUDBotUser(BotUser)
