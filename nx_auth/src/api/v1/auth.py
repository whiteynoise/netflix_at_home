from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body

from models.entity import Users
from schemas.response import Token
from services.auth_service import AuthService, get_auth_service
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from sqlalchemy.exc import IntegrityError

from db.postgres import get_session
from schemas.entity import UserCreate, TokenData
from services.tools import get_current_user

router = APIRouter(tags=['auth'])


@router.post(
    '/register',
    summary='Регистрация пользователя',
    description='Регистрирует пользователя в системе',
    response_model=bool,
)
async def register(
        user: Annotated[UserCreate, Body()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Регистрация'''

    try:
        await auth_service.register(user, db)
        return True
    
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Current user already exists."
        )


@router.post(
    '/login',
    summary='Логин пользователя',
    description='Url для получения токенов для входа в систему',
    response_model=Token,
)
async def login(
        get_user: Annotated[TokenData, Body()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Логин'''
    logger.error(f"Login user {get_user.email} {get_user.username}")
    user: Users | None = await auth_service.identificate_user(get_user, db)

    if not user:
        logger.error(f"User {user.email} {user.username} not found")
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User with this email or username does not exists"
        )
    if not await auth_service.check_password(get_user.password, user):
        logger.error(f"Wrong password")
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Wrong password."
        )

    tokens = await auth_service.token(user, db)

    return tokens


@router.post(
    '/logout',
    summary='Логауит пользователя',
    description='Логаутит пользователя. Удаляет его токены'
)
async def logout(
    db: Annotated[AsyncSession, Depends(get_session)],

):
    '''Логаут'''
    pass


@router.post(
    '/full_logout',
    summary='Логауит пользователя',
    description='Логаутит пользователя. Удаляет его токены'
)
async def full_logout(
    db: Annotated[AsyncSession, Depends(get_session)]
):
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
