from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from services.tools import get_current_user


router = APIRouter(tags=['managment'])


@router.post(
    '/create_role',
    summary='Создание роли',
    description='Создание роли для пользователя'
)
async def create_role(
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[AsyncSession, Depends(get_current_user)]
):
    '''Создание роли'''
    pass


@router.delete(
    '/delete_role/{role_id}',
    summary='Удаление роли',
    description='Удаление роли пользователя'
)
async def delete_role(
    role_id,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[AsyncSession, Depends(get_current_user)]
):
    '''Удаление роли'''
    pass


@router.put(
    '/change_role/{role_id}',
    summary='Изменение роли',
    description='Изменение роли пользователя'
)
async def change_role(
    role_id,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[AsyncSession, Depends(get_current_user)]
):
    '''Изменение роли'''
    pass


@router.get(
    '/get_roles',
    summary='Получение всех ролей',
    description='Получение всех ролей пользователя'
    )
async def get_roles(
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[AsyncSession, Depends(get_current_user)]
):
    '''Получение всех ролей'''
    pass
