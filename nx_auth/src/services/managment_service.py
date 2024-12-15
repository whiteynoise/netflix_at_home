from functools import lru_cache

from db.postgres import get_session
from services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

class ManagementService(BaseService):
    def __int__(self, storage):
        super().__init__(storage)

    async def create_role(self, user, role_title: str):
        pass

    async def delete_role(self, user, role_id):
        pass

    async def change_role(self, user, role_id):
        pass

    async def get_roles(self, user):
        pass

@lru_cache()
def get_management_service(session: AsyncSession = Depends(get_session)) -> ManagementService:
    return ManagementService(session)
