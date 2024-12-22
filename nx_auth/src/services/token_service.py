from functools import lru_cache

from core.config import settings
from db.postgres import get_session
from schemas.entity import TokenData
from services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


class TokenService(BaseService):
    expire = settings.access_token_expire_minute

    def __init__(self, storage):
        super().__init__(storage)

    async def renew_access_token(self, user):
        token = TokenData(username=user.username, email=user.email)
        self.generate_access_token(token)
        pass

    def generate_access_token(self, token: TokenData):
        ## тут надо юзать expire
        pass


@lru_cache()
def get_token_service() -> TokenService:
    return TokenService()
