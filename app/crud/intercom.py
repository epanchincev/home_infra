from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .base import CRUDBase
from app.models import Intercom


class CRUDIntercom(CRUDBase):
    """CRUD операции для домофона"""
    
    @staticmethod
    async def get_intercom_id_by_name(
        intercom_name: str,
        session: AsyncSession,
    ) -> int:
        """Получить id домофона по имени"""
        intercom_exists = await session.execute(
            select(Intercom.id).where(
                Intercom.name == intercom_name
            )
        )

        return intercom_exists.scalars().all()
    
    @staticmethod
    async def get_intercom_id_by_intercom_id(
        intercom_id: int,
        session: AsyncSession,
    ) -> int:
        """Получить id домофона по id домофона в эртелекоме."""
        intercom_exists = await session.execute(
            select(Intercom.id).where(
                Intercom.intercom_id == intercom_id
            )
        )

        return intercom_exists.scalars().all()



intercom_crud = CRUDIntercom(Intercom)
