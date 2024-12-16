from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from services.auth_service import AuthService, get_auth_service
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from schemas.entity import UserAuth, UserCreate

router = APIRouter(tags=['auth'])


@router.post(
    '/register',
    summary='Регистрация пользователя',
    description='Регистрирует пользователя в системе',
    response_model=bool,
)
async def register(
    user: UserCreate,
    film_service: AuthService = Depends(get_auth_service),
):
    '''Регистрация'''

    response: bool = await film_service.register(user)

    if not response:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="User with this email or username already exists."
        )
    
    return response



@router.post(
    '/login',
    summary='Логин пользователя',
    description='Отдает токены пользователю для входа в систему'
    )
async def login(db: Annotated[AsyncSession, Depends(get_session)], user: UserAuth):
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

