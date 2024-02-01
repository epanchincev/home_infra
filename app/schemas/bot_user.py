from pydantic import BaseModel, Field


class BotUserBase(BaseModel):

    id: int
    first_name: str = Field(max_length=64)
    last_name: str = Field(max_length=64)
    username: str = Field(max_length=64)
    
    
class BotUserCreate(BotUserBase):
    """Создание пользователя бота"""
    pass


class BotUserUpdate(BotUserBase):
    """Обновление пользователя бота"""
    pass
    

class BotUserDB(BotUserBase):
    """ Из БД"""
    
    class Config:
        
        orm_modet: True
