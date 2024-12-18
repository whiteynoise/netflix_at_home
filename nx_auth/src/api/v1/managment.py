from uuid import UUID
from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

from models.entity import Roles, user_roles
from schemas.entity import ChangeRole, AddUserRoles, CreateRole
from schemas.response import GetRolesResponse
from services.managment_service import ManagementService, get_management_service
from db.postgres import get_session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

router = APIRouter(tags=['managment'])


@router.post(
    '/create_role',
    summary='Создание роли',
    description='Создание роли для пользователя'
)
async def create_role(
        role: Annotated[CreateRole, Body()],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Создание роли'''
    try:
        await management_service.create_role(**role.model_dump(), db=db)
        return True
    except IntegrityError as e:
        logger.error(f"Current role already exists: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Current role already exists."
        )
    except Exception as e:
        logger.error(f"Error during create role: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error during create role."
        )


@router.delete(
    '/delete_role/{role_id}',
    summary='Удаление роли',
    description='Удаление роли'
)
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
    try:
        await management_service.delete_role(role, db=db)
        return True
    except Exception as e:
        logger.error(f"Error during delete role: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error during delete role."
        )


@router.delete(
    '/delete_role/{user_id}/{role_id}',
    summary='Удаление роли у пользователя',
    description='Удаление роли у пользователя'
)
async def delete_user_role(
        params: Annotated[AddUserRoles, Depends()],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    if not await management_service.get_user_info_by_id(user_id=params.user_id, db=db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )

    if not await management_service.get_role_info_by_id(role_id=params.role_id, db=db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Role not found."
        )

    query = select(user_roles).where(
        user_roles.c.user_id == params.user_id,
        user_roles.c.role_id == params.role_id,
    )

    result = await db.execute(query)
    user_role = result.scalar_one_or_none()
    logger.info(f"User-role: {user_role}")

    if not user_role:
        logger.error(f"Current user have not got current role")
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Current user have not got current role"
        )
    try:
        await management_service.delete_user_role(user_role, db=db)
        return True
    except Exception as e:
        logger.error(f"Error during delete role from user: {str(e)}")
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Error during delete role from user"
        )


@router.put(
    '/change_role',
    summary='Изменение роли',
    description='Изменение роли',
    response_model=bool
)
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
            detail="Nothing was updated. The role was probably not found."
        )

    return True


@router.post(
    '/add_role_to_user',
    summary='Добавить роль пользователю',
    description='Добавить роль пользователю',
    response_model=bool
)
async def add_role_to_user(
        params: Annotated[AddUserRoles, Depends()],
        management_service: Annotated[ManagementService, Depends(get_management_service)],
        db: Annotated[AsyncSession, Depends(get_session)],
):
    '''Добавить роль пользователю.'''

    if not await management_service.get_user_info_by_id(user_id=params.user_id, db=db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )

    if not await management_service.get_role_info_by_id(role_id=params.role_id, db=db):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Role not found."
        )

    return await management_service.add_role_to_user(data_to_add=params.model_dump(), db=db)


@router.get(
    '/get_all_roles',
    summary='Получение всех ролей',
    description='Получение всех ролей в системе',
    response_model=list[GetRolesResponse]
)
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
