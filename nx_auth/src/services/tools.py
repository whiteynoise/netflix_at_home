from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Header
from http import HTTPStatus

from core.config import settings
from db.postgres import get_session
import jwt
from jwt import PyJWTError

from schemas.entity import Token


async def get_current_user(
        access_token: Annotated[str, Header(alias='Authorization')],
):
    '''Получение пользователя по токену'''
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # TODO проверка в редисе что токен не в блеклисте
        payload = jwt.decode(
            access_token,
            settings.secret_key,
            algorithms=[settings.algorithm],
        )
        token = Token(
            user_id=payload.get("user_id"),
            email=payload.get("email"),
            username=payload.get("username"),
        )

        if not token.email or not token.username:
            return credentials_exception

    except PyJWTError:
        raise credentials_exception

    return token


async def authenticate_user(
    db: Annotated[AsyncSession, Depends(get_session)], username: str, password: str
):
    '''Аунтификация пользователя'''
    pass
