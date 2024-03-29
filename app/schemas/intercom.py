from pydantic import BaseModel


class IntercomBase(BaseModel):
    """Базовая модель схемы домофона"""
    
    name: str
    intercom_id: int
    

class IntercomCreate(IntercomBase):
    """Модель создания домофона"""
    pass


class IntercomUpdate(IntercomBase):
    """Модель обновления домофона"""
    pass


class IntercomDB(IntercomBase):
    """Просмотр домофона"""
    
    id: int
    

    def __str__(self) -> str:
        return f'{self.id}: {self.name}'

    class Config:
        
        from_attributes = True
