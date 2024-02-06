from app.models import BotUser

from .base import CRUDBase


class CRUDBotUser(CRUDBase):
    """CRUD для пользователей бота"""
    
    pass


bot_user_crud = CRUDBotUser(BotUser)
