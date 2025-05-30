from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from models.response_models import FilmWork
from services.film import FilmService, film_service
from src.api.v1.constants import SORT_CHOICES
from src.models.entity_models import SearchParams, SortFilms
from src.models.response_models import Film
from src.services.cacher import redis_caching

from models.entity_models import GetFilmIds

from nx_content.src.models.entity_models import SimpleFilmWork

router = APIRouter()


@router.get(
    "/{film_id}",
    response_model=FilmWork,
    summary="Информация о фильме",
    description="Возращает информацию о фильме по id",
)
@redis_caching(key_base="movies_uuid_", response_model=FilmWork, only_one=True)
async def film_details(
    film_id: str, film_service: FilmService = Depends(film_service.get_service)
) -> FilmWork:
    """Возвращает информацию о кинопроизведении"""

    film = await film_service.get_by_id(film_id)

    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="film not found")
    return film


@router.get(
    "/get_fav_films",
    summary="Получить любимые фильмы пользователя",
    description="Возвращает список всех любимых фильмов пользователя с полной информацией",
    response_model=list[FilmWork],
)
async def get_films_by_ids(
    film_service: Annotated[FilmService, Depends(film_service.get_service)],
    films: Annotated[GetFilmIds, Query()],
) -> list[SimpleFilmWork]:

    film_ids: list[str] = await film_service.get_films_by_ids(films.film_ids)

    if not film_ids:
        return []
    films = await film_service.get_films_by_ids(film_ids)
    return films


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
