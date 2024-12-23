import datetime
from functools import lru_cache
from typing import Annotated
from fastapi import Depends

from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.future import select
from sqlalchemy import insert, and_

from core.config import settings
from schemas.entity import UserCreate, TokenData
from schemas.response import Token
from db.const import constants
from loguru import logger

from models.entity import Users, LoginHistory, user_roles

from services.token_service import TokenService, get_token_service


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
    async def check_password(password: str, user: Users):
        return user.check_password(password)


    async def token(
            self,
            user: Users,
            db: AsyncSession,
            token_service: Annotated[TokenService, Depends(get_token_service)]
    ) -> Token:
        '''Отдает токены для пользователя в системе.'''
        logger.info(f'Generate token for: {user.username}, {user.email}')
        payload = {
            'user_id': str(user.user_id),
            'username': user.username,
            'email': user.email,
            'exp': datetime.datetime.now() + datetime.timedelta(minutes=settings.access_token_expire_minutes)
        }
        access_token, refresh_token = token_service.generate_access_refresh_token(payload)

        await db.execute(
            insert(LoginHistory)
            .values(user_id=user.user_id, token=refresh_token)
        )

        return Token(access_token=access_token, refresh_token=refresh_token)



@lru_cache()
def get_auth_service() -> AuthService:
    return AuthService()
