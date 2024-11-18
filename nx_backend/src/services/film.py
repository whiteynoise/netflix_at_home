from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.entity_models import FilmWork
from services.utils.paginator_ import paginator


class FilmService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[FilmWork]:
        '''Получение кинопроизведения по id'''
        film = await self._get_film_from_elastic(film_id)

        if not film:
            return
        
        return film

    async def search_films(
        self, get_query: str | None, page_number: int | None, page_size: int | None
    ) -> list[FilmWork] | None:
        '''Поиск фильмов в Elasticsearch с поддержкой пагинации.'''

        page_number, page_size, offset = paginator(page_number, page_size)

        search_query = {
            'from': offset,
            'size': page_size,
        }

        if get_query:
            search_query['query'] = {'bool': {'must': [{'match': {'title': get_query}}]}}

        result = await self.elastic.search(index='movies', body=search_query)

        hits = result.get('hits', {}).get('hits', [])

        if not hits:
            return

        return [FilmWork(**hit['_source']) for hit in hits]

    async def sorted_films(
        self,
        sort: str,
        genre: str | None,
        page_number: int,
        page_size: int,
    ) -> list[FilmWork] | None:
        '''Отдает фильмы посорченные по заданному полю и отфильтрованные по жанрам'''

        sort_order = 'desc' if sort[0] == '-' else 'asc'
        sort = sort.lstrip('-')

        page_number, page_size, offset = paginator(page_number, page_size)

        search_query = {
            'from': offset,
            'size': page_size,
            'sort': [{sort: {'order': sort_order}}],
            'query': {'bool': {'must': [], 'filter': []}},
        }

        if genre:
            search_query['query']['bool']['filter'].append({'term': {'genres': genre}})

        result = await self.elastic.search(index='movies', body=search_query)

        hits = result.get('hits', {}).get('hits', [])
        if not hits:
            return

        return [FilmWork(**hit['_source']) for hit in hits]

    async def _get_films_by_person(self, person_id) -> list[FilmWork] | None:
        '''Возращает найденные фильмы по личности'''
        search_query = {
            'query': {
                'bool': {
                    'should': [
                        {
                            'nested': {
                                'path': 'directors',
                                'query': {'term': {'directors.id': person_id}},
                            }
                        },
                        {
                            'nested': {
                                'path': 'actors',
                                'query': {'term': {'actors.id': person_id}},
                            }
                        },
                        {
                            'nested': {
                                'path': 'writers',
                                'query': {'term': {'writers.id': person_id}},
                            }
                        },
                    ]
                }
            }
        }
        result = await self.elastic.search(index='movies', body=search_query)
        hits = result.get('hits', {}).get('hits', [])
        if not hits:
            return

        return [FilmWork(**hit['_source']) for hit in hits]

    async def _get_film_from_elastic(self, film_id: str) -> FilmWork | None:
        '''Получение кинопроизведения из ElasticSearch'''
        try:
            doc = await self.elastic.get(index='movies', id=film_id)
        except NotFoundError:
            return
        return FilmWork(**doc['_source'])


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> FilmService:
    return FilmService(elastic)
