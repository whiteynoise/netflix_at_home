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
