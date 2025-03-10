from http import HTTPStatus
from secrets import token_urlsafe
from typing import Annotated

from constants import RoleName
from db.postgres import get_session
from fastapi import APIRouter, Body, Depends, Header, HTTPException
from integration.outer_oauth import get_user_info_oauth
from jwt import InvalidSignatureError
from loguru import logger
from models.entity import Users
from schemas.entity import (PaginatedParams, TokenData, TokenPayload,
                            UserChangeInfo, UserCreate, UserShortData)
from schemas.integration import UniUserOAuth
from schemas.response import History, SocialNetworks, Token, UserLoginFullInfo
from services.auth_service import AuthService, get_auth_service
from services.managment_service import (ManagementService,
                                        get_management_service)
from services.permissions import required
from services.token_service import TokenService, get_token_service
from services.tools import get_current_user
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["auth"])


@router.post(
    "/register",
    summary="Регистрация пользователя",
    description="Регистрирует пользователя в системе",
    response_model=bool,
)
async def register(
    user: Annotated[UserCreate, Body()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> bool:
    """Регистрация"""
    logger.info('{"message": "Hello"}')

    try:
        await auth_service.register(user, db)
        return True

    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Current user already exists."
        )


@router.post(
    "/register_via_oauth",
    summary="Регистрация пользователя через внешний OAuth",
    description="Регистрирует пользователя посредством входа через внешний Oauth",
    response_model=bool,
)
async def register_via_oauth(
    oauth_token: Annotated[str, Header(alias="Authorization")],
    provider: str,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> bool:
    """Регистрация через внешний OAuth."""

    user_info: UniUserOAuth = await get_user_info_oauth(
        provider=provider, oauth_token=oauth_token
    )

    username, email = user_info.username, user_info.email

    if await auth_service.identificate_user(user=TokenData(username=username), db=db):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT, detail="Current user already exists."
        )

    user = UserCreate(
        username=username,
        email=email or f"{token_urlsafe(5)}@netflix_at_home.com",
        first_name=user_info.first_name,
        last_name=user_info.last_name,
        password=token_urlsafe(16),
        outer_oauth_only=True,
    )

    await auth_service.register(user=user, db=db, provider=provider)
    return True


@router.post(
    "/login_via_oauth",
    summary="Логин через внешний OAuth",
    description="Вход в сервис посредством входа через внешний OAuth",
    response_model=Token,
)
async def login_via_oauth(
    oauth_token: Annotated[str, Header(alias="Authorization")],
    provider: str,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    management_service: Annotated[ManagementService, Depends(get_management_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> Token:
    """Логин через внешний OAuth."""

    user_info: UniUserOAuth = await get_user_info_oauth(
        provider=provider, oauth_token=oauth_token
    )

    user: Users | None = await auth_service.identificate_user(
        user=TokenData(username=user_info.username), db=db
    )

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User with this email or username doesn't exist.",
        )

    tokens: Token = await auth_service.login(
        db=db,
        user=user,
        token_service=token_service,
        management_service=management_service,
    )

    return tokens


@router.post(
    "/login",
    summary="Логин пользователя",
    description="Url для получения токенов для входа в систему",
    response_model=Token,
)
async def login(
    get_user: Annotated[TokenData, Body()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    management_service: Annotated[ManagementService, Depends(get_management_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> Token:
    """Логин"""

    user: Users | None = await auth_service.identificate_user(get_user, db)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User with this email or username does not exists",
        )
    if not await auth_service.check_password(get_user.password, user):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Wrong password."
        )

    tokens = await auth_service.login(user, db, token_service, management_service)
    return tokens


@router.post(
    "/extra_login",
    summary="Логин пользователя для внутренних сервисов",
    description="Url для получения токенов для входа в систему для сервисов",
    response_model=UserLoginFullInfo,
)
async def extra_login(
    get_user: Annotated[UserShortData, Body()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    management_service: Annotated[ManagementService, Depends(get_management_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> UserLoginFullInfo:
    """Логин для сервисов (передаем ЛИБО е-mail либо юзернейм)"""
    logger.info("User: %s" % get_user.username)

    user: Users | None = await auth_service.identificate_user(get_user, db)

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User with this email or username does not exists",
        )
    if not await auth_service.check_password(get_user.password, user):
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="Wrong password."
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
        is_superuser=user.is_superuser,
    )


@router.post(
    "/logout",
    summary="Логаутит пользователя",
    description="Логаутит пользователя",
)
@required([RoleName.BASE_USER])
async def logout(
    user: Annotated[TokenPayload, Depends(get_current_user)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    """Логаут"""

    await token_service.revoke_refresh(id_user=user.id_user, db=db)

    await token_service.revoke_access(
        access_token=user.token, detail_message="Logout by user"
    )

    raise HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Logout",
    )


@router.patch(
    "/change_user/{user_id}",
    summary="Изменяет информацию о пароле и логине",
    description="Изменяет информацию о пароле и логине",
    response_model=dict,
)
@required([RoleName.BASE_USER])
async def change_user_info(
    user: Annotated[TokenPayload, Depends(get_current_user)],
    change_info: Annotated[UserChangeInfo, Body()],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> dict:
    """Смена информации о пользователе"""

    if not change_info.username and not change_info.email and not change_info.password:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail="Email or username or password must be in form",
        )

    data = change_info.model_dump(exclude_none=True)

    if await auth_service.update_user(user.user_id, data, db):
        try:
            return {
                "access_token": await token_service.generate_new_access(
                    user.token, data
                )
            }
        except InvalidSignatureError:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST, detail="Incorrect data"
            )

    raise HTTPException(
        status_code=HTTPStatus.UNPROCESSABLE_ENTITY, detail="failed update user info"
    )


@router.get(
    "/enter_history",
    summary="История входов в аккаунт",
    description="История входов в аккаунт",
    response_model=list[History],
)
@required([RoleName.BASE_USER])
async def enter_history(
    user: Annotated[TokenPayload, Depends(get_current_user)],
    pagination: Annotated[PaginatedParams, Depends()],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> list[History]:
    """История входов в аккаунт"""

    return await auth_service.get_login_history(
        user_id=user.user_id, pagination=pagination, db=db
    )


@router.get(
    "/social_networks",
    summary="Список привязанных соц.сетей",
    description="Получить список привязанных соц.сетей",
    response_model=list[SocialNetworks],
)
@required([RoleName.BASE_USER])
async def social_networks(
    user: Annotated[TokenPayload, Depends(get_current_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
) -> list[SocialNetworks]:
    """Получить список привязанных соц.сетей."""

    return await auth_service.get_user_social_networks(user_id=user.user_id, db=db)
