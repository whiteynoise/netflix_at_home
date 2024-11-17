from pydantic import BaseModel


class Film(BaseModel):
    id: str
    title: str
    imdb_rating: float | None
