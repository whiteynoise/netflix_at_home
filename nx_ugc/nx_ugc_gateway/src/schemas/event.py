from pydantic import BaseModel


class BaseEvent(BaseModel):
    topic: str
    method: str
    payload: dict
