from datetime import datetime, timezone
from pydantic import BaseModel, Field
from typing import List


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


class LikeResp(BaseModel):
    ...


class ReviewResp(BaseModel):
    ...
