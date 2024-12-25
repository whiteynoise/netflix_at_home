import jwt
import datetime

from fastapi import HTTPException
from functools import lru_cache
from http import HTTPStatus

from sqlalchemy import select, update, and_
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from db.redis import get_redis
from schemas.entity import TokenData
from services.storage import get_redis_storage
from models.entity import LoginHistory


class TokenService:

    def get_default_expire(self, access: bool = True):
        '''Получение дефолтного expire для аксеса/рефреша'''

        minutes = (
            settings.access_token_expire_minutes if access else
            settings.refresh_token_expire_minutes
        )
        return datetime.datetime.now() + datetime.timedelta(minutes=minutes)

    def generate_access_refresh_token(self, payload) -> tuple[str, str]:
        '''Генерация пары токенов'''

        payload['exp'] = self.get_default_expire()
        access_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        del payload['roles']

        payload['exp'] = self.get_default_expire(access=False)
        refresh_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        return access_token, refresh_token

    async def generate_new_access(
            self,
            token: str,
            get_payload: dict,
            from_refresh: bool = False
        ) -> str:
        '''Генерация нового аксеса на базе старого аксеса или рефреша'''

        await self.revoke_access(access_token=token)

        data: dict = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        new_payload: dict = {
            'user_id': data.get('user_id'),
            'username': get_payload.get('username') or data.get('username'),
            'email': get_payload.get('email') or data.get('email'),
            'exp': self.get_default_expire() if from_refresh else data.get('exp'),
            'roles': get_payload.get('roles') or data.get('roles')
        }
        
        new_access_token: str = jwt.encode(
            new_payload,
            settings.secret_key,
            algorithm=settings.algorithm
        )

        return new_access_token
    
    async def revoke_access(self, access_token: str):
        '''Отзыв аксеса путем добавления его в блэклист'''
        redis_storage = get_redis_storage(await get_redis())
        await redis_storage.add_in_blacklist(access_token)

    async def revoke_refresh(self, id_user: str, db: AsyncSession) -> None:
        '''Отзыв рефреша путем аннулирования активности в БД'''
        await db.execute(
            update(LoginHistory)
            .where(id_user=id_user)
            .values(is_active=False)
        )
    
    async def get_refresh_from_db(self, refresh_token: str, db: AsyncSession):
        '''Проверка активности рефреша в БД'''
        return (
            await db.execute(
                select(LoginHistory)
                .where(
                    and_(
                        LoginHistory.refresh_token == refresh_token,
                        LoginHistory.is_active.is_(True)
                    )
                )
            )
        ).scalars().first()

@lru_cache()
def get_token_service() -> TokenService:
    return TokenService()
