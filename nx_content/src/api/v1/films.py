from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from models.response_models import FilmWork
from src.models.entity_models import SearchParams, SortFilms
from src.services.cacher import redis_caching
from services.film import FilmService, film_service
from src.api.v1.constants import SORT_CHOICES
from src.models.response_models import Film

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=FilmWork,
    summary="Информация о фильме",
    description="Возращает информацию о фильме по id",
)
@redis_caching(key_base="movies_uuid_", response_model=FilmWork, only_one=True)
async def film_details(
    film_id: str,
    film_service: FilmService = Depends(film_service.get_service)
) -> FilmWork:
    """Возвращает информацию о кинопроизведении"""

    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film


@router.get(
    "/search/",
    response_model=list[Film],
    summary="Поиск по фильмам",
    description="Ищет кинопроизведения по названию.",
)
@redis_caching(key_base="movies_search_", response_model=Film)
async def film_search(
    params: SearchParams = Depends(),
    film_service: FilmService = Depends(film_service.get_service),
) -> list[Film]:
    """Ищет кинопроизведения по названию"""

    films = await film_service.search_films(
        params.query, params.page_number, params.page_size
    )

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    return [
        Film(id=str(film.id), title=film.title, imdb_rating=film.imdb_rating)
        for film in films
    ]


@router.get(
    "/",
    response_model=list[Film],
    summary="Самые популярные фильмы",
    description="Возращает популярные фильмы и фильтруте по жанрам",
)
@redis_caching(key_base="movies_main_", response_model=Film)
async def sorted_films(
    params: SortFilms = Depends(),
    film_service: FilmService = Depends(film_service.get_service),
) -> list[Film]:
    """Возращает популярные фильмы и фильтруте по жанрам"""

    if params.sort not in SORT_CHOICES:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="invalid sort parametr"
        )

    films = await film_service.sorted_films(**params.model_dump())

    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")

    return [
        Film(id=str(film.id), title=film.title, imdb_rating=film.imdb_rating)
        for film in films
    ]
