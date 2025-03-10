from typing import List
from pydantic import BaseModel, Field


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


class CreateLike(BaseModel):
    review_id: str
    action: bool


# review
class LikeEntry(BaseModel):
    user_id: str
    action: bool


class UpdateReview(BaseModel):
    review_text: str = None
    rating_by_user: str = None


class CreateReview(BaseModel):
    film_id: str
    review_text: str
    rating_by_user: int
