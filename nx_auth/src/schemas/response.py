from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel


class GetRolesResponse(BaseModel):
    role_id: UUID
    title: str

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    refresh_token: str


class UserLoginFullInfo(BaseModel):
    user_id: UUID
    username: str
    email: str
    first_name: str
    last_name: str
    roles: List[str]
    is_active: bool
    is_stuff: bool
    is_superuser: bool


class History(BaseModel):
    log_id: UUID
    login_date: datetime

    class Config:
        orm_mode = True


class SocialNetworks(BaseModel):
    user_social_id: UUID
    user_id: UUID
    provider: str

    class Config:
        orm_mode = True
