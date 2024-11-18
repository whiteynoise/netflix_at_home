from functools import lru_cache
from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.entity_models import Genres


class GenreService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, genre_id: str) -> Genres | None:
        '''Получение информации жанра по id'''
        genre = await self._get_genre_from_elastic(genre_id)
        if not genre:
            return
        return genre

    async def get_genres(self) -> list[Genres] | None:
        'Отдает все жанры'
        search_query = {'query': {'match_all': {}}}
        result = await self.elastic.search(index='genres', body=search_query)
        hits = result['hits']['hits']
        if not hits:
            return
        genres = [Genres(**hit['_source']) for hit in hits]
        return genres

    async def _get_genre_from_elastic(self, genre_id: str) -> Genres | None:
        '''Получение жанра из ElasticSearch'''
        try:
            doc = await self.elastic.get(index='genres', id=genre_id)
        except NotFoundError:
            return
        return Genres(**doc['_source'])


@lru_cache()
def get_film_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> GenreService:
    return GenreService(elastic)
