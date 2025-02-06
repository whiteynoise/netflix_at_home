import secrets
from http import HTTPStatus
from typing import Annotated

from jwt import InvalidSignatureError
from fastapi import APIRouter, Depends, HTTPException, Body
from loguru import logger

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from constants import RoleName

from models.entity import Users
from db.postgres import get_session

from schemas.response import Token, History, UserLoginFullInfo
from schemas.entity import UserCreate, TokenData, UserChangeInfo, TokenPayload, PaginatedParams, UserShortData

from services.auth_service import AuthService, get_auth_service
from services.managment_service import ManagementService, get_management_service
from services.permissions import required
from services.token_service import TokenService, get_token_service
from services.tools import get_current_user

from integration.yandex import get_user_info_yndx

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
    '/register_via_yndx',
    summary='Регистрация пользователя через Яндекс',
    description='Регистрирует пользователя посредством входа через Яндекс',
    response_model=bool,
)
async def register_via_yndx(
        yndx_data: Annotated[dict, Depends(get_user_info_yndx)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Регистрация через Яндекс.'''

    login, email = yndx_data['login'], yndx_data['default_email']

    if await auth_service.identificate_user(
        user=TokenData(username=login, email=email), db=db
    ):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Current user already exists."
        )
    
    user = UserCreate(
        username=login,
        email=email,
        first_name=yndx_data.get('first_name'),
        last_name=yndx_data.get('last_name'),
        password=secrets.token_urlsafe(16)
    )

    await auth_service.register(user=user, db=db)
    return True


@router.post(
    '/login_via_yndx',
    summary='Логин через Яндекс',
    description='Вход в сервис посредством входа через Яндекс',
    response_model=Token,
)
async def login_via_yndx(
        yndx_data: Annotated[dict, Depends(get_user_info_yndx)],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        token_service: Annotated[TokenService, Depends(get_token_service)],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    """Логин через Яндекс."""

    user: Users | None = await auth_service.identificate_user(
        user=TokenData(username=yndx_data['login'], email=yndx_data['default_email']),
        db=db
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User with this email or username doesn't exist."
        )
    
    tokens: Token = await auth_service.login(
        db=db,
        user=user,
        token_service=token_service,
        management_service=management_service
    )

    return tokens


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

    user: Users | None = await auth_service.identificate_user(get_user, db)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User with this email or username does not exists"
        )
    if not await auth_service.check_password(get_user.password, user):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Wrong password."
        )

    tokens = await auth_service.login(user, db, token_service, management_service)
    return tokens


@router.post(
    '/extra_login',
    summary='Логин пользователя для внутренних сервисов',
    description='Url для получения токенов для входа в систему для сервисов',
    response_model=UserLoginFullInfo,
)
async def extra_login(
        get_user: Annotated[UserShortData, Body()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
) -> UserLoginFullInfo:
    '''Логин для сервисов (передаем ЛИБО е-mail либо юзернейм)'''
    logger.info("User: %s" % get_user.username)

    user: Users | None = await auth_service.identificate_user(get_user, db)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User with this email or username does not exists"
        )
    if not await auth_service.check_password(get_user.password, user):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Wrong password."
        )

    roles = await management_service.get_user_roles(user_id=user.user_id, db=db)
    roles = [role.title for role in roles]

    logger.info("USER: %s %s" % (roles, user.user_id))
    return UserLoginFullInfo(
        user_id=user.user_id,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name,
        roles=roles,
        is_active=user.is_active,
        is_stuff=user.is_stuff,
        is_superuser=user.is_superuser
    )


@router.post(
    '/logout',
    summary='Логаутит пользователя',
    description='Логаутит пользователя'
)
@required([RoleName.BASE_USER])
async def logout(
        user: Annotated[TokenPayload, Depends(get_current_user)],
        token_service: Annotated[TokenService, Depends(get_token_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Логаут'''
    
    await token_service.revoke_refresh(
        id_user=user.id_user,
        db=db
    )

    await token_service.revoke_access(
        access_token=user.token,
        detail_message='Logout by user'
    )

    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail='Logout',
    )


@router.patch(
    '/change_user/{user_id}',
    summary='Изменяет информацию о пароле и логине',
    description='Изменяет информацию о пароле и логине',
    response_model=dict
)
@required([RoleName.BASE_USER])
async def change_user_info(
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

    if await auth_service.update_user(user.user_id, data, db):
        try:
            return {
                'access_token': await token_service.generate_new_access(user.token, data)
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
@required([RoleName.BASE_USER])
async def enter_history(
        user: Annotated[TokenPayload, Depends(get_current_user)],
        pagination: Annotated[PaginatedParams, Depends()],
        auth_service: Annotated[AuthService, Depends(get_auth_service)],
        db: Annotated[AsyncSession, Depends(get_session)]
):
    '''История входов в аккаунт'''

    return await auth_service.get_login_history(
        user_id=user.user_id,
        pagination=pagination,
        db=db
    )
