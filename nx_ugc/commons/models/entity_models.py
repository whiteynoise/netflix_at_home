from typing import List
from pydantic import BaseModel, Field


class TokenPayload(BaseModel):
    user_id: str
    username: str
    email: str
    roles: List[str]
    token: str


# BASE
class UserBase(BaseModel):
    user_id: str


class UserFilmBase(UserBase):
    film_id: str


class ReviewUserBase(UserBase):
    review_id: str


# BOOKMARK
class BookmarkBase(UserBase):
    bookmark_name: str


class AddToBookmark(UserFilmBase):
    film_name: str


class DelFromBookmark(BookmarkBase):
    film_ids: list[str]


# RATING
class RatingChange(UserFilmBase):
    rating: int = Field(ge=1, le=10)


# REVIEW
class AddReview(UserFilmBase):
    review_text: str
    rating_by_user: int


class UpdReview(ReviewUserBase):
    review_text: str | None = None
    rating_by_user: str | None = None


# LIKE
class AddLike(ReviewUserBase):
    action: bool


class LikeEntry(UserBase):
    action: bool
