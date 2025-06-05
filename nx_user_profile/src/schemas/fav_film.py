import uuid

from pydantic import BaseModel, ConfigDict


class FilmBody(BaseModel):
    film_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class FavFilmCreate(BaseModel):
    user_id: uuid.UUID
    film_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)


class FilmWork(BaseModel):
    id: uuid.UUID
    imdb_rating: float | None
    title: str

    model_config = ConfigDict(from_attributes=True)
