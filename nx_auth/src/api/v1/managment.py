from http import HTTPStatus

from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.entity import ChangeRole, AddUserRoles
from schemas.response import GetRolesResponse
from services.managment_service import ManagementService, get_management_service
from db.postgres import get_session
from services.tools import get_current_user


router = APIRouter(tags=['managment'])


@router.post(
    '/create_role',
    summary='Создание роли',
    description='Создание роли для пользователя'
)
async def create_role(
    management_service: ManagementService = Depends(get_management_service),
):
    '''Создание роли'''
    pass


@router.delete(
    '/delete_role/{role_id}',
    summary='Удаление роли',
    description='Удаление роли пользователя'
)
async def delete_role(
    role_id,
    db: Annotated[AsyncSession, Depends(get_session)],
    current_user: Annotated[AsyncSession, Depends(get_current_user)]
):
    '''Удаление роли'''
    pass


@router.put(
    '/change_role',
    summary='Изменение роли',
    description='Изменение роли',
    response_model=bool
)
async def change_role(
    role: ChangeRole = Depends(),
    management_service: ManagementService = Depends(get_management_service),
):
    '''Изменение роли.'''

    result = await management_service.change_role(**role.model_dump())

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
    params: AddUserRoles = Depends(),
    management_service: ManagementService = Depends(get_management_service),
):
    '''Добавить роль пользователю.'''

    if not await management_service.get_user_info_by_id(user_id=params.user_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="User not found."
        )

    if not await management_service.get_role_info_by_id(role_id=params.role_id):
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Role not found."
        )
    
    return await management_service.add_role_to_user(data_to_add=params.model_dump())


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
    