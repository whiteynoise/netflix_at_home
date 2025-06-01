from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session
from models import UserProfile
from schemas.user import UserProfileUpdate

router = APIRouter()


@router.patch('/profile/{user_id}', response_model=UserProfileUpdate)
async def update_user_profile(
        user_id: UUID,
        data: UserProfileUpdate,
        db: AsyncSession = Depends(get_session),
) -> UserProfileUpdate:
    """Обновление профиля пользователя"""
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail='Профиля не существует')

    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(profile, field, value)

    await db.commit()
    await db.refresh(profile)
    return data


@router.get('/profile/{user_id}', response_model=UserProfileUpdate)
async def get_user_profile(
        user_id: UUID,
        db: AsyncSession = Depends(get_session),
) -> UserProfileUpdate:
    """Получение профиля пользователя"""
    result = await db.execute(select(UserProfile).where(UserProfile.user_id == user_id))
    profile = result.scalar_one_or_none()

    if not profile:
        raise HTTPException(status_code=404, detail='Профиля не существует')

    return UserProfileUpdate.model_validate(profile)