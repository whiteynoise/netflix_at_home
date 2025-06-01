from typing import List
from uuid import UUID

from pydantic import BaseModel
from src.models.utils_models import PaginatedParams


class SearchParams(PaginatedParams):
    query: str | None = None


class SortFilms(PaginatedParams):
    sort: str = "-imdb_rating"
    genre: str | None = None


class PersonBase(BaseModel):
    id: UUID
    name: str


class FilmWork(BaseModel):
    id: UUID
    imdb_rating: float | None
    genres: list
    title: str
    description: str | None

    directors_names: list
    actors_names: list
    writers_names: list

    directors: list[PersonBase]
    actors: list[PersonBase]
    writers: list[PersonBase]


class SimpleFilmWork(BaseModel):
    id: UUID
    imdb_rating: float | None
    title: str


class Genres(BaseModel):
    id: UUID
    name: str
    description: str | None


class PersonFilms(BaseModel):
    id: UUID
    roles: list


class Persons(PersonBase):
    films: list[PersonFilms]


class TokenPayload(BaseModel):
    user_id: str
    username: str
    email: str
    roles: List[str]
    token: str


class GetFilmIds(BaseModel):
    film_ids: list[str]
