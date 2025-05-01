import datetime

from pydantic import BaseModel, ConfigDict


class CreateEventSchema(BaseModel):
    template_id: str
    user_id: str | None = None
    title: str
    description: str | None
    time: datetime.datetime | None = None
    volume_type: str
    roles: list[str]

    model_config = ConfigDict(use_enum_values=True)