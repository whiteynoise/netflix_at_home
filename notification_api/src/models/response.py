import datetime

from pydantic import BaseModel

from models.constants import VolumeEventType, NotificationEventType


class EventCreate(BaseModel):
    template_id: str | None = None
    user_id: str | None = None
    title: str
    msg_text: str | None = None
    time: datetime.datetime | None
    volume_type: VolumeEventType
    notification_type: NotificationEventType
    roles: list[str]
