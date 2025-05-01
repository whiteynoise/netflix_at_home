import datetime
from uuid import UUID

from pydantic import BaseModel, model_validator

from api.v1.constants import EventType


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
    type: str
    roles: list[str]

    @model_validator(mode="after")
    def validate_time_type(self):
        if self.type == EventType.REGULAR.value and self.time is None:
            raise ValueError("Регулярные события должны быть со временем.")
        if self.type == EventType.INSTANCE.value and self.time is not None:
            raise ValueError("Мгновенные события не должны содержать время.")
        return self

    @model_validator(mode="after")
    def validate_type(self):
        if self.type not in (EventType.REGULAR.value, EventType.INSTANCE.value):
            raise ValueError("Такого типа события не существует")
        return self


    class Config:
        orm_mode = True
