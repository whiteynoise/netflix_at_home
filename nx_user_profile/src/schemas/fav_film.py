import uuid

from pydantic import BaseModel


class FilmBody(BaseModel):
    film_id: uuid.UUID


class FavFilmCreate(BaseModel):
    user_id: uuid.UUID
    film_id: uuid.UUID

    class Config:
        orm_mode = True


class FilmWork(BaseModel):
    id: uuid.UUID
    imdb_rating: float | None
    title: str

    class Config:
        orm_mode = True
