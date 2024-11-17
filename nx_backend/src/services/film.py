from functools import lru_cache
from typing import Optional

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from redis.asyncio import Redis

from db.elastic import get_elastic
from db.redis import get_redis
from models.entity_models import FilmWork

FILM_CACHE_EXPIRE_IN_SECONDS = 60 * 5  # 5 минут


class FilmService:
    def __init__(self, redis: Redis, elastic: AsyncElasticsearch):
        self.redis = redis
        self.elastic = elastic

    async def get_by_id(self, film_id: str) -> Optional[FilmWork]:
        '''Получение кинопроизведения по id'''
        film = await self._get_film_from_elastic(film_id)
        if not film:
            return
        return film

    async def search_films(
        self, get_query: str, page_number: int | None, page_size: int | None
    ) -> list[FilmWork] | None:
        '''Поиск фильмов в Elasticsearch с поддержкой пагинации.'''

        page_number, page_size, offset = self.paginator(page_number, page_size)

        search_query = {
            'from': offset,
            'size': page_size,
            'query': {'bool': {'must': [{'match': {'title': get_query}}]}},
        }

        result = await self.elastic.search(index='movies', body=search_query)

        hits = result.get('hits', {}).get('hits', [])
        if not hits:
            return

        return [FilmWork(**hit['_source']) for hit in hits]

    async def sorted_films(
        self,
        sort,
        genre,
        page_number,
        page_size,
    ) -> list[FilmWork] | None:
        '''Отдает фильмы посорченные по заданному полю и отфильтрованные по жанрам'''

        sort_order = 'desc' if sort[0] == '-' else 'asc'
        sort = sort.lstrip('-')

        page_number, page_size, offset = self.paginator(page_number, page_size)

        search_query = {
            'from': offset,
            'size': page_size,
            'sort': [{sort: {'order': sort_order}}],
            'query': {'bool': {'must': [], 'filter': []}},
        }
        if genre:
            search_query['query']['bool']['filter'].append(
                {'term': {'genres': genre}}
            )

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
            return None
        return FilmWork(**doc['_source'])

    async def _film_from_cache(self, film_id: str) -> FilmWork | None:
        '''Получение кинопроизведения из Redis'''
        data = await self.redis.get(film_id)
        if not data:
            return
        film = FilmWork.model_validate_json(data)
        return film

    async def _put_film_to_cache(self, film: FilmWork):
        '''Сохранение данных в кэше Redis'''
        await self.redis.set(
            str(film.id), film.model_dump_json(), FILM_CACHE_EXPIRE_IN_SECONDS
        )
    
    @staticmethod
    def paginator(page_number: int | None, page_size: int | None):
        page_number = page_number or 1
        page_size = page_size or 50

        # считаю смещение вручную
        offset = (page_number - 1) * page_size
        return page_number, page_size, offset


@lru_cache()
def get_film_service(
    redis: Redis = Depends(get_redis),
    elastic: AsyncElasticsearch = Depends(get_elastic),
) -> FilmService:
    return FilmService(redis, elastic)
