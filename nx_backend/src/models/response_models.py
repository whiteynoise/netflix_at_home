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

    @field_validator('id', mode='before')
    def double(value: UUID) -> str:
        return str(value)


class Person(BaseModel):
    id: str
    name: str
    films: list[PersonFilm]

    @field_validator('id', mode='before')
    def double(value: UUID) -> str:
        return str(value)
