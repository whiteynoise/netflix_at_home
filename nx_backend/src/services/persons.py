from functools import lru_cache

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends

from db.elastic import get_elastic
from models.entity_models import Persons


class PersonService:
    def __init__(self, elastic: AsyncElasticsearch):
        self.elastic = elastic

    async def get_by_id(self, person_id: str) -> Persons | None:
        '''Получение личности по id'''
        person = await self._get_person_from_elastic(person_id)
        if not person:
            return
        return person

    async def search_persons(
        self, get_query: str | None, page_number: int | None, page_size: int | None
    ) -> list[Persons] | None:
        '''Поиск личностей в Elasticsearch с поддержкой пагинации.'''

        page_number, page_size, offset = self.paginator(page_number, page_size)

        search_query = {
            'from': offset,
            'size': page_size,
        }

        if get_query:
            search_query['query'] = {'bool': {'must': [{'match': {'name': get_query}}]}}

        result = await self.elastic.search(index='persons', body=search_query)

        hits = result.get('hits', {}).get('hits', [])
        if not hits:
            return

        return [Persons(**hit['_source']) for hit in hits]

    async def _get_person_from_elastic(self, person_id: str) -> Persons | None:
        '''Получение личности из ElasticSearch'''
        try:
            doc = await self.elastic.get(index='persons', id=person_id)
        except NotFoundError:
            return None
        return Persons(**doc['_source'])

    @staticmethod
    def paginator(page_number: int | None, page_size: int | None):
        page_number = page_number or 1
        page_size = page_size or 50

        # считаю смещение вручную
        offset = (page_number - 1) * page_size
        return page_number, page_size, offset


@lru_cache()
def get_person_service(
    elastic: AsyncElasticsearch = Depends(get_elastic)
) -> PersonService:
    return PersonService(elastic)
