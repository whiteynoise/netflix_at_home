from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException


from services.film import FilmService, get_film_service
from src.models.response_models import Film

router = APIRouter()


@router.get(
    '/{film_id}',
    response_model=Film,
    summary='Информация о фильме',
    description='Возращает информацию о фильме по id',
)
async def film_details(
    film_id: str, film_service: FilmService = Depends(get_film_service)
) -> Film:
    '''Возвращает информацию о кинопроизведении'''
    film = await film_service.get_by_id(film_id)
    if not film:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return Film(id=str(film.id), title=film.title, imdb_rating=film.imdb_rating)


@router.get(
    '/search/',
    response_model=list[Film],
    summary='Поиск по фильмам',
    description='Ищет кинопроизведения по названию.',
)
async def film_search(
    query: str = None,
    page_number: int = None,
    page_size: int = None,
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    '''Ищет кинопроизведения по названию'''
    films = await film_service.search_films(query, page_number, page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return [
        Film(id=str(film.id), title=film.title, imdb_rating=film.imdb_rating)
        for film in films
    ]


@router.get(
    '/',
    response_model=list[Film],
    summary='Самые популярные фильмы',
    description='Возращает популярные фильмы и фильтруте по жанрам',
)
async def sorted_films(
    sort: str = '-imdb_rating',
    genre: str = None,
    page_number: int = None,
    page_size: int = None,
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    '''Возращает популярные фильмы и фильтруте по жанрам'''
    films = await film_service.sorted_films(sort, genre, page_number, page_size)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return [
        Film(id=str(film.id), title=film.title, imdb_rating=film.imdb_rating)
        for film in films
    ]
