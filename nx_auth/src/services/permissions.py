from functools import wraps
from http import HTTPStatus
from typing import Callable
from fastapi import HTTPException
from loguru import logger

from schemas.entity import TokenPayload


def auth_required(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        logger.info("AUTH")
        user: TokenPayload = kwargs.get("user")
        roles: list = user.roles
        logger.info(f"Check role {roles} about {user.username}")

        if "base_user" in roles:
            return await func(*args, **kwargs)
        raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Access denied'
            )
    return wrapper


def admin_required(func: Callable):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user: TokenPayload = kwargs.get("user")
        roles: list = user.roles

        if "admin" in roles:
            return await func(*args, **kwargs)
        raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail='Access denied'
            )
    return wrapper
