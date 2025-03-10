from http import HTTPStatus
from typing import Annotated

import jwt
from core.config import settings
from db.redis import get_redis
from fastapi import Header, HTTPException
from jwt import ExpiredSignatureError, PyJWTError
from schemas.entity import TokenPayload
from services.storage import get_redis_storage


async def get_current_user(
    jwt_token: Annotated[str, Header(alias="Authorization")],
) -> TokenPayload | HTTPException:
    """Получение пользователя по токену"""

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    redis_storage = get_redis_storage(await get_redis())

    if await redis_storage.check_in_blacklist(jwt_token):
        raise credentials_exception

    try:
        payload = jwt.decode(
            jwt_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )

        token = TokenPayload(
            user_id=payload["user_id"],
            email=payload["email"],
            username=payload["username"],
            roles=payload.get("roles"),
            token=jwt_token,
        )

    except ExpiredSignatureError:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
    except (PyJWTError, KeyError):
        raise credentials_exception

    return token
