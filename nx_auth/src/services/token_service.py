import datetime
from functools import lru_cache
from http import HTTPStatus

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
        del payload['roles']
        payload['exp'] = datetime.datetime.now() + datetime.timedelta(minutes=settings.refresh_token_expire_minutes)
        refresh_token = jwt.encode(payload, settings.secret_key, algorithm=settings.algorithm)

        return access_token, refresh_token

    def generate_new_payload_access(self, access_token, get_payload):
        # TODO старый токен кинуть в блеклист

        data = jwt.decode(
            access_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        new_access_token_data = {
            'user_id': data.get('user_id'),
            'username': get_payload.get('username') or data.get('username'),
            'email': get_payload.get('email') or data.get('email'),
            'exp': data.get('exp'),
        }
        new_access_token_data = jwt.encode(new_access_token_data, settings.secret_key, algorithm=settings.algorithm)
        return new_access_token_data

@lru_cache()
def get_token_service() -> TokenService:
    return TokenService()
