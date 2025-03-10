from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from services.token_service import TokenService, get_token_service
from schemas.entity import TokenPayload

from services.managment_service import ManagementService, get_management_service
from services.token_service import TokenService, get_token_service
from services.tools import get_current_user

router = APIRouter(tags=["token"])


@router.post(
    "/refresh_access_token",
    summary="Обновление аксеса по рефрешу",
    description="Обновление аксесс токена по рефреш токену",
)
async def refresh_access_token(
    user: Annotated[TokenPayload, Depends(get_current_user)],
    token_service: Annotated[TokenService, Depends(get_token_service)],
    management_service: Annotated[ManagementService, Depends(get_management_service)],
    db: Annotated[AsyncSession, Depends(get_session)],
):
    """Обновление аксесс токена по рефреш токену"""

    refresh_token = user.token

    if not await token_service.get_refresh_from_db(refresh_token=refresh_token, db=db):
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED, detail="Invalid or missing token."
        )

    roles = management_service.get_user_roles(user_id=user.user_id, db=db)

    access_token = await token_service.generate_new_access(
        token=refresh_token,
        get_payload={"roles": [role.title for role in roles]},
        from_refresh=True,
    )

    return {"access_token": access_token}


@router.get(
    "/get_user_from_token",
    summary="Получение информации по юзеру из токена",
    description="Проверка аксесса и получение информации из него по юзеру",
)
async def get_user_from_token(
    user: Annotated[TokenPayload, Depends(get_current_user)],
):
    return user
