from sqlalchemy import Column, String, Text

from app.core.db import Base


class SomeData(Base):
    """Какие-то данные, временный класс"""
    
    name = Column(String(256), unique=True, nullable=False)
    description = Column(Text)
