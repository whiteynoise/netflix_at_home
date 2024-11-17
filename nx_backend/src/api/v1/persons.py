from http import HTTPStatus
from fastapi import APIRouter, Depends, HTTPException


from models.entity_models import Persons
from services.persons import PersonService, get_person_service
from services.film import FilmService, get_film_service
from models.response_models import Film, Person, PersonFilm

router = APIRouter()


@router.get(
    '/{person_id}',
    response_model=Persons,
    summary='Информация о личности',
    description='Возращает информацию о личности по id',
)
async def film_details(
    person_id: str, person_service: PersonService = Depends(get_person_service)
) -> Persons:
    '''Возвращает информацию о личности'''
    person = await person_service.get_by_id(person_id)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return person


@router.get(
    '/search/',
    response_model=list[Person],
    summary='Поиск по личностям',
    description='Ищет личностей по имени.',
)
async def person_search(
    query: str = None,
    page_number: int = None,
    page_size: int = None,
    person_service: PersonService = Depends(get_person_service),
) -> list[Person]:
    '''Ищет личностей по имени'''
    persons = await person_service.search_persons(query, page_number, page_size)
    if not persons:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return [
        Person(
            id=str(person.id),
            name=person.name,
            films=[
                PersonFilm(id=str(film.id), roles=film.roles) for film in person.films
            ],
        )
        for person in persons
    ]


@router.get(
    '/{person_id}/film/',
    response_model=list[Film],
    summary='Фильмы по личности',
    description='Возращает фильмы по личности',
)
async def film__by_person(
    person_id: str,
    film_service: FilmService = Depends(get_film_service),
) -> list[Film]:
    '''Возращает фильмы по личности'''
    films = await film_service._get_films_by_person(person_id)
    if not films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='film not found')

    return [
        Film(id=str(film.id), title=film.title, imdb_rating=film.imdb_rating)
        for film in films
    ]
