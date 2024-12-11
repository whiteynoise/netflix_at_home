from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from db.postgres import get_session


async def get_current_user(token):
    '''Получение пользователя по токену'''
    pass


async def authenticate_user(
    db: Annotated[AsyncSession, Depends(get_session)], username: str, password: str
):
    '''Аунтификация пользователя'''
    pass