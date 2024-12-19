from uuid import UUID
from functools import lru_cache
from sqlalchemy import select, insert, update, asc, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.entity import Users, Roles, user_roles
from loguru import logger


class ManagementService:

    async def create_role(self, role_title: str, db: AsyncSession):
        '''Создание роли'''
        await db.execute(insert(Roles).values(title=role_title))

    async def delete_role(self, role, db: AsyncSession):
        '''Удаление роли'''
        await db.delete(role)

    async def delete_user_role(self, user_id: UUID, role_id: UUID, db: AsyncSession):
        '''Удаление роли у конкретного пользователя'''
        return (
            await db.execute(
                delete(user_roles)
                .where(
                    (user_roles.c.user_id == user_id) &
                    (user_roles.c.role_id == role_id)
                )
                .returning(user_roles.c.user_id)
            )
        ).scalars().first()

    async def get_user_info_by_id(self, user_id: UUID, db: AsyncSession):
        '''Получение информации о пользователе по его uuid.'''
        return (
            await db.execute(
                select(Users)
                .filter(Users.user_id == user_id)
            )
        ).scalars().first()

    async def get_role_info_by_id(self, role_id: UUID, db: AsyncSession):
        '''Получение информации о роли по ее uuid.'''
        return (
            await db.execute(
                select(Roles)
                .filter(Roles.role_id == role_id)
            )
        ).scalars().first()

    async def change_role(self, role_id: UUID, title: str, db: AsyncSession):
        '''Изменение роли.'''
        returned_value = (
            await db.execute(
                update(Roles)
                .where(Roles.role_id == role_id)
                .values(title=title)
                .returning(Roles.role_id)
            )
        ).scalars().first()

        return returned_value

    async def add_role_to_user(self, data_to_add: dict, db: AsyncSession):
        '''Добавить роль пользователю.'''
        await db.execute(
            insert(user_roles)
            .values(data_to_add)
        )

        return True

    async def get_all_roles(self, db: AsyncSession):
        '''Получение всех ролей в системе.'''
        return (
            await db.execute(
                select(Roles)
                .order_by(asc(Roles.title))
            )
        ).scalars().all()

    async def get_user_roles(self, user_id: UUID, db: AsyncSession):
        '''Получение всех ролей пользователя.'''
        return (
            await db.execute(
                select(Roles)
                .select_from(user_roles)
                .join(Roles, user_roles.c.role_id == Roles.role_id)
                .filter(user_roles.c.user_id == user_id)
                .order_by(asc(Roles.title))
            )
        ).scalars().all()


@lru_cache()
def get_management_service() -> ManagementService:
    return ManagementService()
