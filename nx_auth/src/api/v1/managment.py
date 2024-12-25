from uuid import UUID
from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from models.entity import Roles
from schemas.entity import ChangeRole, AddUserRoles, CreateRole, TokenPayload
from schemas.response import GetRolesResponse
from services.managment_service import ManagementService, get_management_service
from db.postgres import get_session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from loguru import logger

from services.permissions import required
from services.tools import get_current_user

router = APIRouter(tags=['managment'])


@router.post(
    '/create_role',
    summary='Создание роли',
    description='Создание роли для пользователя'
)
@required(["admin"])
async def create_role(
        role: Annotated[CreateRole, Body()],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Создание роли'''

    try:
        return await management_service.create_role(**role.model_dump(), db=db)
    
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Current role already exists."
        )


@router.delete(
    '/delete_role/{role_id}',
    summary='Удаление роли',
    description='Удаление роли'
)
@required(["admin"])
async def delete_role(
        role_id: UUID,
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    role = await db.execute(select(Roles).where(Roles.role_id == role_id))
    role = role.scalar_one_or_none()

    if not role:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail=f"Role with id {role_id} does not exists."
        )

    await management_service.delete_role(role, db=db)

    return True


@router.delete(
    '/delete_role',
    summary='Удаление роли у пользователя',
    description='Удаление роли у пользователя',
    response_model=dict
)
@required(["admin"])
async def delete_user_role(
        user: Annotated[TokenPayload, Depends(get_current_user)],
        params: Annotated[AddUserRoles, Body()],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Удаление роли'''

    if not await management_service.get_user_info_by_id(user_id=params.user_id, db=db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )

    if not (role := await management_service.get_role_info_by_id(role_id=params.role_id, db=db)):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Role not found."
        )
    logger.info(f"{user.roles}, {role.title}")
    try:
        payload = {
            'roles': user.roles.remove(role.title)
        }
        access_token = await management_service.generate_new_payload_access(user.token, payload)
        result = await management_service.delete_user_role(**params.model_dump(), db=db)
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Current user already has certain role."
        )
    except ValueError:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Current role not in verify."
        )

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Current user hasn't current role"
        )
    return {"access_token": access_token}


@router.put(
    '/change_role',
    summary='Изменение роли',
    description='Изменение роли',
    response_model=bool
)
@required(["admin"])
async def change_role(
        role: Annotated[ChangeRole, Depends()],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Изменение роли.'''

    result = await management_service.change_role(**role.model_dump(), db=db)

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Nothing was updated. The role wasn't found."
        )

    return True


@router.post(
    '/add_role_to_user',
    summary='Добавить роль пользователю',
    description='Добавить роль пользователю',
    response_model=dict
)
@required(["admin"])
async def add_role_to_user(
        user: Annotated[TokenPayload, Depends(get_current_user)],
        params: Annotated[AddUserRoles, Body()],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Добавить роль пользователю.'''

    if not await management_service.get_user_info_by_id(user_id=params.user_id, db=db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )

    if not (role := await management_service.get_role_info_by_id(role_id=params.role_id, db=db)):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Role not found."
        )

    try:
        payload = {
            'roles': user.roles.append(role.title)
        }
        access_token = await management_service.generate_new_payload_access(user.token, payload)
        await management_service.add_role_to_user(data_to_add=params.model_dump(), db=db)
        return {"access_token": access_token}
    
    except IntegrityError:
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Current user already has certain role."
        )


@router.get(
    '/get_all_roles',
    summary='Получение всех ролей',
    description='Получение всех ролей в системе',
    response_model=list[GetRolesResponse]
)
@required(["admin"])
async def get_all_roles(
        management_service: ManagementService = Depends(get_management_service),
):
    '''Получение всех ролей'''

    result = await management_service.get_all_roles()

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="No roles found."
        )

    return result


@router.get(
    '/get_user_roles/{user_id}',
    summary='Получение ролей пользователя',
    description='Получение всех ролей пользователя',
    response_model=list[GetRolesResponse]
)
@required(["admin"])
async def get_user_roles(
        user_id: str,
        management_service: ManagementService = Depends(get_management_service),
):
    '''Получение всех ролей пользователя'''

    result = await management_service.get_user_roles(user_id=user_id)

    if not result:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User doesn't have any roles or doesn't exist."
        )

    return result
