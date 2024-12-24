import datetime
from functools import lru_cache
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy import insert, and_, update, desc

from core.config import settings
from db.redis import get_redis
from schemas.entity import UserCreate, TokenData
from db.const import constants
from schemas.response import Token
from loguru import logger

from models.entity import Users, LoginHistory, user_roles
from services.managment_service import ManagementService
from services.storage import get_redis_storage

from services.token_service import TokenService


class AuthService:

    async def register(self, user: UserCreate, db: AsyncSession) -> None:
        '''Метод регистрации пользователя.'''
        
        new_user = Users(**user.model_dump())
        db.add(new_user)
        
        await db.flush()

        await db.execute(
            insert(user_roles)
            .values(
                user_id=new_user.user_id,
                role_id=constants.roles.get('base_user')
            )
        )

    async def logout(self, user):
        pass

    @staticmethod
    async def identificate_user(user: TokenData, db: AsyncSession):
        '''Индетификация пользователя на основе юзернейма и почты'''

        logger.info(f'Identificate_user: {user.username}, {user.email}')
        query = select(Users).where(
            and_(Users.username == user.username, Users.email == user.email)
        )
        result = await db.execute(query)
        user = result.scalar_one_or_none()
        return user

    @staticmethod
    async def check_password(password: str, user: Users):
        return user.check_password(password)

    async def login(
            self,
            user: Users,
            db: AsyncSession,
            token_service: TokenService,
            management_service: ManagementService,
    ) -> Token:
        '''Отдает токены для пользователя в системе.'''
        logger.info(f'Generate token for: {user.username}, {user.email}')

        roles = await management_service.get_user_roles(user.user_id, db)

        payload = {
            'user_id': str(user.user_id),
            'username': user.username,
            'email': user.email,
            'roles': [role.title for role in roles],
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=settings.access_token_expire_minutes)
        }
        access_token, refresh_token = token_service.generate_access_refresh_token(payload)

        await db.execute(
            insert(LoginHistory)
            .values(user_id=user.user_id, token=refresh_token)
        )

        redis_storage = get_redis_storage(await get_redis())
        await redis_storage.set_value(str(user.user_id), access_token)

        return Token(access_token=access_token, refresh_token=refresh_token)

    async def update_user(self, user_id: UUID, data: dict, db: AsyncSession):
        '''Обновление пользователя'''
        query = update(Users).where(Users.user_id == user_id).values(**data)
        await db.execute(query)
        return True

    async def get_login_history(self, user_id: UUID, db: AsyncSession):
        '''Получает историю входов в систему'''
        query = select(LoginHistory).where(LoginHistory.user_id == user_id).order_by(desc(LoginHistory.login_date))
        result = await db.scalars(query)
        return result


@lru_cache()
def get_auth_service() -> AuthService:
    return AuthService()
