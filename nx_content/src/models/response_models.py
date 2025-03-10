from uuid import UUID

from pydantic import BaseModel, field_validator


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: float | None


class Genre(BaseModel):
    id: str
    name: str


class PersonFilm(BaseModel):
    id: str
    roles: list

    @field_validator("id", mode="before")
    def change_uuid_to_str(value: UUID) -> str:
        return str(value)


class Person(BaseModel):
    id: str
    name: str
    films: list[PersonFilm]

    @field_validator("id", mode="before")
    def change_uuid_to_str(value: UUID) -> str:
        return str(value)


class PersonBase(BaseModel):
    id: str
    name: str


class FilmWork(BaseModel):
    id: str
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
