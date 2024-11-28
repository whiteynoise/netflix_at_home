from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException

from services.genre import GenreService, genre_service
from src.services.cacher import redis_caching
from src.models.response_models import Genre

router = APIRouter()


@router.get(
    '/{genre_id}',
    response_model=Genre,
    summary='Информация о жанре',
    description='Возращает информацию о жанре по id',
)
@redis_caching(key_base='genres_uuid_', response_model=Genre, only_one=True)
async def genre_getails(
    genre_id: str,
    genre_service: GenreService = Depends(genre_service.get_service)
) -> Genre:
    '''Возращает информацию о жанре по id'''
    genre = await genre_service.get_by_id(genre_id)

    if not genre:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='genre not found')
    
    return Genre(id=str(genre.id), name=genre.name)


@router.get(
    '/',
    response_model=list[Genre],
    summary='Список жанров',
    description='Возращает список жанров',
)
@redis_caching(key_base='genres_main_', response_model=Genre)
async def genres(
    genre_service: GenreService = Depends(genre_service.get_service),
) -> list[Genre]:
    '''Возращает список всех жанров'''
    genres = await genre_service.get_genres()
    return [Genre(id=str(genre.id), name=genre.name) for genre in genres]
