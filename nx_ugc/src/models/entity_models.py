from datetime import datetime, timezone
from uuid import UUID
from pydantic import BaseModel, Field
from typing import List


class TokenPayload(BaseModel):
    user_id: str
    username: str
    email: str
    roles: List[str]
    token: str


class BookmarkBase(BaseModel):
    bookmark_name: str


class BookmarkAdd(BookmarkBase):
    film_id: str
    film_name: str


class BookmarkDel(BookmarkBase):
    film_ids: list[str]


class RatingBase(BaseModel):
    film_id: str


class RatingAdd(RatingBase):
    film_name: str
    rating: int = Field(ge=1, le=10)


class RatingUpd(RatingBase):
    rating: int = Field(ge=1, le=10)


class RatingGet(BaseModel):
    film_id: str | None = None
