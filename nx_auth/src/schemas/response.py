from datetime import datetime
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


class History(BaseModel):
    log_id: str
    login_date: datetime

    class Config:
        orm_mode = True

