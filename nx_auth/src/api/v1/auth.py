
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session


router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/register',
    summary='Регистрация пользователя',
    description='Регистрирует пользователя в системе'
)
async def register(db: Annotated[AsyncSession, Depends(get_session)], user):
    '''Регистрация'''
    pass


@router.post(
    '/login',
    summary='Логин пользователя',
    description='Отдает токены пользователю для входа в систему'
    )
async def login(db: Annotated[AsyncSession, Depends(get_session)]):
    '''Логин'''
    pass


@router.post(
    '/logout',
    summary='Логауит пользователя',
    description='Логаутит пользователя. Удаляет его токены'
    )
async def logout(db: Annotated[AsyncSession, Depends(get_session)]):
    '''Логаут'''
    pass


@router.post(
    '/change_user',
    summary='Изменяет информацию о пароле и логине',
    description='Изменяет информацию о пароле и логине'
    )
async def change_user_info(db: Annotated[AsyncSession, Depends(get_session)]):
    '''Смена информации о пользователе'''
    pass


@router.post(
    '/enter_history',
    summary='История входов в аккаунт',
    description='История входов в аккаунт'
    )
async def enter_history(db: Annotated[AsyncSession, Depends(get_session)]):
    '''История входов в аккаунт'''
    pass

