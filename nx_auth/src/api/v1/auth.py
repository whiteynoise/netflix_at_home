from http import HTTPStatus

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Body

from models.entity import Users
from schemas.response import Token, History
from services.auth_service import AuthService, get_auth_service
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from sqlalchemy.exc import IntegrityError

from jwt import InvalidSignatureError
from db.postgres import get_session
from schemas.entity import UserCreate, TokenData, UserChangeInfo, UserHistory, TokenPayload
from services.managment_service import ManagementService, get_management_service
from services.permissions import required
from services.token_service import TokenService, get_token_service
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
        token_service: Annotated[TokenService, Depends(get_token_service)],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Логин'''
    logger.error(f"Login user {get_user.email} {get_user.username}")
    user: Users | None = await auth_service.identificate_user(get_user, db)

    if not user:
        logger.error(f"User {get_user.email} {get_user.username} not found")
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

    tokens = await auth_service.login(user, db, token_service, management_service)
    return tokens


@router.post(
    '/logout',
    summary='Логаутит пользователя',
    description='Логаутит пользователя. Удаляет его токены'
)
async def logout(
    get_user: Annotated[TokenData, Body()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    db: Annotated[AsyncSession, Depends(get_session)],

):
    '''Логаут'''
    # TODO тут еще нужно добавлять в блеклист
    pass


@router.post(
    '/full_logout',
    summary='Логаутит пользователя',
    description='Логаутит пользователя. Удаляет его токены'
)
async def full_logout(
    db: Annotated[AsyncSession, Depends(get_session)]
):
    '''Логаут'''
    # TODO тут еще нужно добавлять в блеклист
    # add_in_blacklist
    pass

@router.patch(
    '/change_user/{user_id}',
    summary='Изменяет информацию о пароле и логине',
    description='Изменяет информацию о пароле и логине',
)
@required(["base_user"])
async def change_user_info(
        user_id: UUID,
        user: Annotated[TokenPayload, Depends(get_current_user)],
        change_info: Annotated[UserChangeInfo, Body()],
        token_service: Annotated[TokenService, Depends(get_token_service)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Смена информации о пользователе'''

    if not change_info.username and not change_info.email and not change_info.password:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail='Email or username or password must be in form'
        )

    data = change_info.model_dump(exclude_none=True)

    if await auth_service.update_user(user_id, data, db):
        try:
            return {
                'access_token': await token_service.generate_new_payload_access(user.token, data)
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
@required(["base_user"])
async def enter_history(
        user: Annotated[TokenPayload, Depends(get_current_user)],
        get_user: Annotated[UserHistory, Depends()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        db: Annotated[AsyncSession, Depends(get_session)]
):
    '''История входов в аккаунт'''

    result = await auth_service.get_login_history(get_user.user_id, db)

    history_list = [
        History(
            log_id=str(record.log_id),
            login_date=record.login_date
        )
        for record in result
    ]

    return history_list


