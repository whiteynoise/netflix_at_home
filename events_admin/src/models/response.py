import datetime
from uuid import UUID

from pydantic import BaseModel, model_validator, ConfigDict

from api.v1.constants import TimeEventType, VolumeEventType


class TemplateCommon(BaseModel):
    template_id: UUID
    path: str

    class Config:
        orm_mode = True


class CreateEventSchema(BaseModel):
    template_id: str
    user_id: str | None = None
    title: str
    description: str | None
    time: datetime.datetime | None = None
    volume_type: VolumeEventType
    time_type: TimeEventType
    roles: list[str]

    @model_validator(mode="after")
    def validate_time_type(self):
        if self.time_type == TimeEventType.DEFERRED.value and self.time is None:
            raise ValueError("Отложенные события должны быть со временем.")
        if self.time_type == TimeEventType.INSTANT.value and self.time is not None:
            raise ValueError("Мгновенные события не должны содержать время.")
        return self

    model_config = ConfigDict(use_enum_values=True)