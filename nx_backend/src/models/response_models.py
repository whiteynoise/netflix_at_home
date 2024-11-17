from pydantic import BaseModel


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


class Person(BaseModel):
    id: str
    name: str
    films: list[PersonFilm]
