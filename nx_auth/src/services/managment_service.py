from functools import lru_cache
from uuid import UUID

from models.entity import Roles, Users, user_roles
from services.token_service import TokenService
from sqlalchemy import asc, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class ManagementService(TokenService):

    async def create_role(self, role_title: str, db: AsyncSession) -> None:
        """Создание роли"""
        await db.execute(insert(Roles).values(title=role_title))

    async def delete_role(self, role: Roles, db: AsyncSession) -> None:
        """Удаление роли"""
        await db.delete(role)

    async def delete_user_role(self, user_id: UUID, role_id: UUID, db: AsyncSession) -> int | None:
        """Удаление роли у конкретного пользователя"""
        return (
            (
                await db.execute(
                    delete(user_roles)
                    .where(
                        (user_roles.c.user_id == user_id)
                        & (user_roles.c.role_id == role_id)
                    )
                    .returning(user_roles.c.user_id)
                )
            )
            .scalars()
            .first()
        )

    async def get_user_info_by_id(self, user_id: UUID, db: AsyncSession) -> Users | None:
        """Получение информации о пользователе по его uuid."""
        return (
            (await db.execute(select(Users).filter(Users.user_id == user_id)))
            .scalars()
            .first()
        )

    async def get_role_info_by_id(self, role_id: UUID, db: AsyncSession) -> Roles | None:
        """Получение информации о роли по ее uuid."""
        return (
            (await db.execute(select(Roles).filter(Roles.role_id == role_id)))
            .scalars()
            .first()
        )

    async def change_role(self, role_id: UUID, title: str, db: AsyncSession) -> int | None:
        """Изменение роли."""
        returned_value = (
            (
                await db.execute(
                    update(Roles)
                    .where(Roles.role_id == role_id)
                    .values(title=title)
                    .returning(Roles.role_id)
                )
            )
            .scalars()
            .first()
        )

        return returned_value

    async def add_role_to_user(self, data_to_add: dict, db: AsyncSession) -> bool:
        """Добавить роль пользователю."""
        await db.execute(insert(user_roles).values(data_to_add))

        return True

    async def get_all_roles(self, db: AsyncSession) -> list[Roles]:
        """Получение всех ролей в системе."""
        return (
            (await db.execute(select(Roles).order_by(asc(Roles.title)))).scalars().all()
        )

    async def get_user_roles(self, user_id: UUID, db: AsyncSession) -> list[Roles]:
        """Получение всех ролей пользователя."""
        return (
            (
                await db.execute(
                    select(Roles)
                    .select_from(user_roles)
                    .join(Roles, user_roles.c.role_id == Roles.role_id)
                    .filter(user_roles.c.user_id == user_id)
                    .order_by(asc(Roles.title))
                )
            )
            .scalars()
            .all()
        )


@lru_cache()
def get_management_service() -> ManagementService:
    return ManagementService()
