from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    username: str = Field(..., description="Никнейм")
    password: str = Field(..., min_length=8, max_length=32, description="Пароль")
    first_name: str | None
    last_name: str | None
    email: EmailStr | None


class UserInDB(BaseModel):
    id: UUID
    first_name: str | None
    last_name: str | None

    class Config:
        orm_mode = True

class UserAuth(BaseModel):
    username: str = Field(..., description="Никнейм")
    password: str = Field(..., min_length=8, max_length=32, description="Пароль")


### TOKEN ###

class TokenData(BaseModel):
    user_id: str
    username: str | None