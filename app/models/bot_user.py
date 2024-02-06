from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class BotUser(Base):
    """Пользователь в БД"""
    first_name: Mapped[str | None] = mapped_column(String(64))
    last_name: Mapped[str | None] = mapped_column(String(64))
    username: Mapped[str | None] = mapped_column(String(64))
    
    def __repr__(self) -> str:
        text = f'#️⃣<b>ID:</b> {self.tg_id}\n'

        if self.username:
            text += f'👤<b>username:</b> @{self.username}\n'

        if self.first_name:
            f'1️⃣<b>first_name:</b> {self.first_name}\n'

        if self.last_name:
            text += f'2️⃣<b>last_name:</b> {self.last_name}\n'

        return text
