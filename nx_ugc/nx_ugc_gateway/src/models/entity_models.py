from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: str
    username: str
    email: str
    phone: str | None = None
    roles: list[str]
    token: str
