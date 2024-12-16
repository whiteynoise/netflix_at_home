from functools import lru_cache
from fastapi import Depends
from sqlalchemy import select, insert, update, asc
from sqlalchemy.ext.asyncio import AsyncSession

from models.entity import Users, Roles, user_roles
from db.postgres import get_session
from services.base_service import BaseService


class ManagementService(BaseService):
    def __init__(self, storage):
        super().__init__(storage)

    async def create_role(self, title: str):
        # TODO: доделать
        self.storage.add(Roles(title=title))
        await self.storage.commit()

    async def delete_role(self, user, role_id):
        pass
    
    async def get_user_info_by_id(self, user_id: str):
        '''Получение информации о пользователе по его uuid.'''
        return (
            await self.storage.execute(
                select(Users)
                .filter(Users.user_id == user_id)
            )
        ).scalars().first()

    async def get_role_info_by_id(self, role_id: str):
        '''Получение информации о роли по ее uuid.'''
        return (
            await self.storage.execute(
                select(Roles)
                .filter(Roles.role_id == role_id)
            )
        ).scalars().first()

    async def change_role(self, role_id: str, title: str):
        '''Изменение роли.'''
        returned_value = (
            await self.storage.execute(
                update(Roles)
                .where(Roles.role_id == role_id)
                .values(title=title)
                .returning(Roles.role_id)
            )
        ).scalars().first()

        await self.storage.commit()

        return returned_value

    async def add_role_to_user(self, data_to_add: dict):
        '''Добавить роль пользователю.'''
        await self.storage.execute(
            insert(user_roles)
            .values(data_to_add)
        )
        await self.storage.commit()

        return True

    async def get_all_roles(self):
        '''Получение всех ролей в системе.'''
        return (
            await self.storage.execute(
                select(Roles)
                .order_by(asc(Roles.title))
            )
        ).scalars().all()

    async def get_user_roles(self, user_id: int):
        '''Получение всех ролей пользователя.'''
        return (
            await self.storage.execute(
                select(Roles)
                .select_from(user_roles)
                .join(Roles, user_roles.c.role_id == Roles.role_id)
                .filter(user_roles.c.user_id == user_id)
                .order_by(asc(Roles.title))
            )
        ).scalars().all()

@lru_cache()
def get_management_service(session: AsyncSession = Depends(get_session)) -> ManagementService:
    return ManagementService(session)
