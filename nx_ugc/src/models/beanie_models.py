import uuid
from datetime import datetime

import pymongo
from beanie import Document
from models.entity_models import LikeEntry
from pydantic import Field
from pymongo import IndexModel


class BaseCollection(Document):
    user_id: str
    created_at: datetime = Field(default_factory=lambda: datetime.now())


class Bookmark(BaseCollection):
    bookmark_name: str
    film_id: str
    film_name: str

    class Settings:
        indexes = [
            IndexModel(
                [
                    ("bookmark_name", pymongo.ASCENDING),
                    ("user_id", pymongo.ASCENDING),
                    ("film_id", pymongo.ASCENDING),
                ],
                name="bm_film_user_uq_ASCENDING",
                unique=True,
            ),
        ]


class Rating(BaseCollection):
    film_id: str
    film_name: str
    rating: int
    updated_at: datetime | None = None

    class Settings:
        indexes = [
            IndexModel(
                [
                    ("film_id", pymongo.ASCENDING),
                    ("user_id", pymongo.ASCENDING),
                ],
                name="user_film_uq_ASCENDING",
                unique=True,
            ),
        ]


class Like(BaseCollection):
    review_id: str
    action: bool

    class Settings:
        indexes = [
            IndexModel(
                [
                    ("user_id", pymongo.ASCENDING),
                    ("review_id", pymongo.ASCENDING),
                ],
                name="like_user_review_uq_ASCENDING",
                unique=True,
            ),
        ]


class Review(BaseCollection):
    review_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    film_id: str
    review_text: str
    edited_at: None | datetime = None
    rating_by_user: int
    likes: list[LikeEntry] = Field(default_factory=list)

    class Settings:
        indexes = [
            IndexModel(
                [
                    ("user_id", pymongo.ASCENDING),
                    ("film_id", pymongo.ASCENDING),
                ],
                name="user_review_uq_ASCENDING",
                unique=True,
            ),
        ]
