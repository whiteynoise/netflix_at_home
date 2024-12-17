import datetime
from functools import lru_cache
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy import and_

from core.config import settings
from schemas.entity import UserCreate, TokenData
from schemas.response import Token
from loguru import logger

from models.entity import Users, LoginHistory
import jwt


class AuthService:

    async def register(self, user: UserCreate, db: AsyncSession) -> None:
        '''Метод регистрации пользователя.'''
        db.add(Users(**user.model_dump()))
        await db.commit()

    async def logout(self, user):
        pass

    async def change_user(self, body):
        pass

    async def login_history(self, user):
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
    async def token(user: Users, db: AsyncSession) -> Token:
        '''Отдает токены для пользователя в системе.'''
        logger.info(f'Generate token for: {user.username}, {user.email}')
        payload = {
            'user_id': str(user.user_id),
            'username': user.username,
            'email': user.email,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.access_token_expire_minutes)
        }
        access_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=settings.refresh_token_expire_minutes)
        refresh_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        db.add(
            LoginHistory(
                user_id=user.user_id,
                token=refresh_token
            )
        )
        await db.commit()

        return Token(access_token=access_token, refresh_token=refresh_token)

    @staticmethod
    async def authenticate_user(username: str, password: str):
        user = "взять из бд, если есть -> проверить пароль"
        user.check_password(password)


@lru_cache()
def get_auth_service() -> AuthService:
    return AuthService()
