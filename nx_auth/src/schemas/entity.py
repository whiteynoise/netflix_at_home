from typing import List
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_validator
from werkzeug.security import generate_password_hash


class UserCreate(BaseModel):
    username: str = Field(..., description="Никнейм")
    password: str = Field(..., min_length=8, max_length=32, description="Пароль")
    first_name: str | None = None
    last_name: str | None = None
    email: EmailStr


class UserInDB(BaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None

    class Config:
        orm_mode = True


class UserAuth(BaseModel):
    username: str = Field(..., description="Никнейм")
    password: str = Field(..., min_length=8, max_length=32, description="Пароль")


class UserChangeInfo(BaseModel):
    username: str = None
    email: str = None
    password: str = None

    @field_validator("password", mode="after")
    def hash_password(value: str) -> str:
        return generate_password_hash(value)


class UserChangePassword(BaseModel):
    user_id: UUID
    passwword: str


class UserHistory(BaseModel):
    user_id: UUID

### ROLES ###
class CreateRole(BaseModel):
    role_title: str


class AddUserRoles(BaseModel):
    user_id: UUID
    role_id: UUID


class ChangeRole(BaseModel):
    role_id: UUID
    title: str


### TOKEN ###

class TokenData(BaseModel):
    username: str | None
    email: str | None
    password: str | None

class TokenPayload(BaseModel):
    user_id: str | None
    username: str | None
    email: str | None
    roles: List[str]
    token: str