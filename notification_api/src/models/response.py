import datetime
from uuid import UUID

from pydantic import BaseModel


class EventCreate(BaseModel):
    template_id: str
    user_id: str | None = None
    title: str
    description: str | None
    time: datetime.datetime | None
    type: str
    roles: list[str]


class EventSend(BaseModel):
    template_id: UUID
    time: datetime.datetime | None
    type: str
    roles: list[str]

    class Config:
        orm_mode = True
