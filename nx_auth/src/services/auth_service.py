from functools import lru_cache

from db.postgres import get_session
from schemas.entity import UserCreate, UserInDB
from services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


class AuthService(BaseService):

    def __int__(self, storage):
        super().__init__(storage)

    async def register(self, user: UserCreate) -> UserInDB:
        pass

    async def login(self, username: str, password: str):
        await self.authenticate_user(username, password)
        pass

    async def logout(self, user):
        pass

    async def change_user(self, body):
        pass

    async def enter_history(self, user):
        pass

    async def authenticate_user(self, username: str, password: str):
        user = "взять из бд, если есть -> проверить пароль"
        user.check_password(password)


@lru_cache()
def get_auth_service(session: AsyncSession = Depends(get_session)) -> AuthService:
    return AuthService(session)


