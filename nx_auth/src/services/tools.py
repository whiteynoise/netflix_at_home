from typing import Annotated
from fastapi import HTTPException, Header
from http import HTTPStatus

from core.config import settings
import jwt
from jwt import PyJWTError, ExpiredSignatureError
from loguru import logger

from db.redis import get_redis
from schemas.entity import TokenPayload
from services.storage import get_redis_storage


async def get_current_user(
        access_token: Annotated[str, Header(alias='Authorization')],
):
    '''Получение пользователя по токену'''
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    redis_storage = get_redis_storage(await get_redis())
    if await redis_storage.check_in_blacklist(access_token):
        return credentials_exception
    logger.info(f"Get user {access_token}")

    try:
        payload = jwt.decode(
            access_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        token = TokenPayload(
            user_id=payload.get('user_id'),
            email=payload.get('email'),
            username=payload.get('username'),
            roles=payload.get('roles')
        )

        if not token.email or not token.username:
            return credentials_exception

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED
        )
    except PyJWTError:
        raise credentials_exception

    return token
