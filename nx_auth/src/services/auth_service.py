import datetime
from functools import lru_cache
from uuid import UUID

from constants import TEMPLATE_ID, SINGLE_NOTIFICATION_SERVICE_API
from db.const import constants
from db.redis import get_redis
from models.entity import LoginHistory, Users, UserSocial, user_roles
from schemas.entity import PaginatedParams, TokenData, UserCreate
from schemas.response import Token
from services.managment_service import ManagementService
from services.storage import get_redis_storage
from services.token_service import TokenService
from sqlalchemy import desc, insert, or_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from session import aiohttp_session


class AuthService:
    async def register(
        self, user: UserCreate, db: AsyncSession, provider: str | None = None
    ) -> None:
        """Метод регистрации пользователя."""

        new_user = Users(**user.model_dump())
        db.add(new_user)

        await db.flush()

        await db.execute(
            insert(user_roles).values(
                user_id=new_user.user_id, role_id=constants.roles.get("base_user")
            )
        )

        if provider:
            new_user_social = UserSocial(user_id=new_user.user_id, provider=provider)
            db.add(new_user_social)

        body = {
            "template_id": TEMPLATE_ID,
            "title": f"Регистрация {new_user.user_id}",
            "notification_api": "email",
            "description": None,
            "time": datetime.now().isoformat(),
            "volume_type": "single",
        }
        async with aiohttp_session.post(
            SINGLE_NOTIFICATION_SERVICE_API, json=body
        ) as response:
            if response.status not in (200, 201):
                print(
                    f" Ошибка при отправки события на регистрацию {new_user.user_id}: {response.status}"
                )
                return

    @staticmethod
    async def identificate_user(user: TokenData, db: AsyncSession) -> Users | None:
        """Индетификация пользователя на основе юзернейма и почты"""

        query = select(Users).where(or_(Users.username == user.username))
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user

    @staticmethod
    async def check_password(password: str, user: Users) -> bool:
        return user.check_password(password)

    async def login(
        self,
        user: Users,
        db: AsyncSession,
        token_service: TokenService,
        management_service: ManagementService,
    ) -> Token:
        """Отдает токены для пользователя в системе."""

        roles = await management_service.get_user_roles(user.user_id, db)

        payload = {
            "user_id": str(user.user_id),
            "username": user.username,
            "email": user.email,
            "roles": [role.title for role in roles],
        }
        access_token, refresh_token = token_service.generate_access_refresh_token(
            payload
        )

        await db.execute(
            insert(LoginHistory).values(user_id=user.user_id, token=refresh_token)
        )

        redis_storage = get_redis_storage(await get_redis())
        await redis_storage.set_value(str(user.user_id), access_token)

        return Token(access_token=access_token, refresh_token=refresh_token)

    async def update_user(self, user_id: UUID, data: dict, db: AsyncSession) -> bool:
        """Обновление пользователя"""
        query = update(Users).where(Users.user_id == user_id).values(**data)
        await db.execute(query)
        return True

    async def get_login_history(
        self,
        user_id: UUID,
        pagination: PaginatedParams,
        db: AsyncSession,
    ) -> LoginHistory | None:
        """Получает историю входов в систему"""

        return (
            (
                await db.execute(
                    select(LoginHistory)
                    .where(LoginHistory.user_id == user_id)
                    .order_by(desc(LoginHistory.login_date))
                    .limit(pagination.page_size)
                    .offset((pagination.page_number - 1) * pagination.page_size)
                )
            )
            .scalars()
            .all()
        )

    async def get_user_social_networks(
        self, user_id: UUID, db: AsyncSession
    ) -> UserSocial | None:
        """Получает привязанные соц.сети по пользователю"""

        return (
            (await db.execute(select(UserSocial).where(UserSocial.user_id == user_id)))
            .scalars()
            .all()
        )


@lru_cache()
def get_auth_service() -> AuthService:
    return AuthService()
