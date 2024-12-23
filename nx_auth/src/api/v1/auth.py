from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body

from models.entity import Users
from schemas.response import Token, History
from services.auth_service import AuthService, get_auth_service
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash

from jwt import InvalidSignatureError
from db.postgres import get_session
from schemas.entity import UserCreate, TokenData, UserChangeInfo, UserHistory
from services.token_service import TokenService, get_token_service

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
        token_service: Annotated[TokenService, Depends(get_token_service)],
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

    tokens = await auth_service.token(user, db, token_service)

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


@router.patch(
    '/change_user',
    summary='Изменяет информацию о пароле и логине',
    description='Изменяет информацию о пароле и логине',
)
async def change_user_info(
        change_info: Annotated[UserChangeInfo, Body()],
        token_service: Annotated[TokenService, Depends(get_token_service)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Смена информации о пользователе'''
    data: dict = {}
    username: str = change_info.username
    email: str = change_info.email
    password: str = change_info.password

    if not username and not email and not password:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Email or username or password must be in form'
        )

    if email:
        data['email'] = email
    if username:
        data['username'] = username
    if password:
        data['password'] = generate_password_hash(password)

    if await auth_service.update_user(change_info.user_id, data, db):

        try:
            return {
                'access_token': token_service.generate_new_payload_access(change_info.token, data)
            }
        except InvalidSignatureError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail='Incorrect data'
            )
    raise HTTPException(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
        detail='failed update user info'
    )


@router.get(
    '/enter_history',
    summary='История входов в аккаунт',
    description='История входов в аккаунт',
    response_model=list[History]
)
async def enter_history(
        user: Annotated[UserHistory, Depends()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        db: Annotated[AsyncSession, Depends(get_session)]
):
    '''История входов в аккаунт'''

    result = await auth_service.get_login_history(user.user_id, db)

    history_list = [
        History(
            log_id=str(record.log_id),
            login_date=record.login_date
        )
        for record in result
    ]

    return history_list


