from uuid import UUID
from pydantic import BaseModel

from pydantic_settings import BaseSettings, SettingsConfigDict


class EnvSettings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    redis_host: str
    redis_port: int

    elastic_host: str
    elastic_port: int


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


class Genres(BaseModel):
    id: UUID
    name: str
    description: str | None


class PersonFilms(BaseModel):
    id: UUID
    roles: list


class Person(PersonBase):
    films: list[PersonFilms]


model_by_index = {
    'movies': FilmWork,
    'genres': Genres,
    'persons': Person
}
