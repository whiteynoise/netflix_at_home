import datetime
from uuid import UUID

from pydantic import BaseModel, model_validator

from models.constants import EventType


class EventCreate(BaseModel):
    template_id: str
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
