from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.db import Base


class Intercom(Base):
    """Данные домофонов"""

    intercom_id: Mapped[int] = mapped_column(unique=True)
    intercom_name: Mapped[str] = mapped_column(String(256), unique=True)
