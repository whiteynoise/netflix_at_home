from typing import List
from pydantic import BaseModel


class TokenPayload(BaseModel):
    user_id: str
    username: str
    email: str
    phone: str | None = None
    roles: List[str]
    token: str


class UserProfileUpdate(BaseModel):
    nickname: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    avatar_path: str | None = None
    description: str | None = None
