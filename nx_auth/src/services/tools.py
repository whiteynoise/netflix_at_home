from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, Header
from http import HTTPStatus
from sqlalchemy.future import select
from sqlalchemy import and_

from core.config import settings
from db.postgres import get_session
import jwt
from jwt import PyJWTError

from models.entity import Users


async def get_current_user(
        access_token: Annotated[str, Header(alias='Authorization')],
        db:  Annotated[AsyncSession, Depends(get_session)]
):
    '''Получение пользователя по токену'''
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # TODO проверка в редисе что токен не в блеклисте
        payload = jwt.decode(access_token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("email")
        username: str = payload.get("username")

        if not email or not username:
            return credentials_exception

    except PyJWTError as e:
        raise credentials_exception

    query = select(Users).where(
            and_(Users.username == username, Users.email == email)
        )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception
    return user


async def authenticate_user(
    db: Annotated[AsyncSession, Depends(get_session)], username: str, password: str
):
    '''Аунтификация пользователя'''
    pass
