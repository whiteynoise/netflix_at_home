import datetime
from functools import lru_cache

from core.config import settings
from schemas.entity import TokenData
import jwt


class TokenService:
    expire = settings.access_token_expire_minutes

    async def renew_access_token(self, user):
        token = TokenData(username=user.username, email=user.email)
        self.generate_access_token(token)
        pass

    def generate_access_token(self, token: TokenData):
        ## тут надо юзать expire
        pass

    def generate_access_refresh_token(self, payload):
        access_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)
        payload['exp'] = datetime.datetime.now() + datetime.timedelta(minutes=settings.refresh_token_expire_minutes)
        refresh_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        return access_token, refresh_token


@lru_cache()
def get_token_service() -> TokenService:
    return TokenService()
