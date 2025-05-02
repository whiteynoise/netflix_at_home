import datetime

from pydantic import BaseModel

from models.constants import VolumeEventType


class EventCreate(BaseModel):
    template_id: str
    user_id: str | None = None
    title: str
    description: str | None
    time: datetime.datetime | None
    volume_type: VolumeEventType
    roles: list[str]
