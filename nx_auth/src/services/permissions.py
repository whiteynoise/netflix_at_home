from functools import wraps
from http import HTTPStatus
from typing import Callable
from fastapi import HTTPException

from schemas.entity import TokenPayload
from loguru import logger


def required(verify_roles: list):
    def inner(func: Callable):
        @wraps(func)
        async def wrapper(
            *args,
            **kwargs
        ):
            user: TokenPayload = kwargs.get("user")
            logger.info(f"Check required user {user.username}")
            roles: list = user.roles
            logger.info(f"Check {verify_roles} for {user.username}: roles {user.roles}")
            if any(role in roles for role in verify_roles):
                return await func(*args, **kwargs)
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Access denied'
            )
        return wrapper
    return inner

