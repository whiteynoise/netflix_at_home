from datetime import datetime
from pydantic import BaseModel


class BookmarkResp(BaseModel):
    bookmark_name: str
    user_id: str
    film_id: str
    film_name: str
    created_at: datetime


class RatingResp(BaseModel):
    film_id: str
    user_id: str
    film_name: str
    rating: int
    created_at: datetime


class AvgFilmRating(BaseModel):
    film_id: str
    avg_rating: float


class LikeList(BaseModel):
    user_id: str
    review_id: str
    action: bool
    created_at: datetime

    class Config:
        orm_mode = True


# review
class LikeEntry(BaseModel):
    user_id: str
    action: bool


class ListReview(BaseModel):
    review_id: str
    user_id: str
    film_id: str
    review_text: str
    edited_at: None | datetime
    rating_by_user: int
    likes: list[LikeEntry]
    created_at: datetime
