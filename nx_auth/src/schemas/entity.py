from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


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
    user_id: UUID
    username: str | None
    email: str | None
