from uuid import UUID
from pydantic import BaseModel


class Person(BaseModel):
    id: UUID
    name: str


class FilmWorker(Person):
    film_works: list


class Film(BaseModel):
    id: UUID
    title: str
    description: str
    imdb_rating: float | None
    genres: list
    directors: list[Person]
    actors: list[Person]
    writers: list[Person]
    file_path: str | None

    
class Genres(BaseModel):
    id: UUID
    name: str
    description: str
