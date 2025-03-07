import pymongo
from pymongo import IndexModel

from beanie import Document
from datetime import datetime
from pydantic import Field
from typing import List


class BaseCollection(Document):
    user_id: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now()
    )


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
    ...


class Review(BaseCollection):
    ...
