from db.elastic import get_elastic
from models.response_models import Person
from services.abstract_models import ServiceManager, Storage
from services.utils.paginator_ import get_offset


class PersonService:
    def __init__(self, storage: Storage):
        self.storage = storage

    async def get_by_id(self, person_id: str) -> Person | None:
        '''Получение личности по id'''
        person = await self._get_person_from_storage(person_id)
        if not person:
            return
        return person

    async def search_persons(
        self, get_query: str | None, page_number: int, page_size: int
    ) -> list[Person] | None:
        '''Поиск личностей в хранилище с поддержкой пагинации.'''

        offset = get_offset(page_number, page_size)

        search_query = {
            'from': offset,
            'size': page_size,
        }

        if get_query:
            search_query['query'] = {'bool': {'must': [{'match': {'name': get_query}}]}}

        result = await self.storage.search(index='persons', body=search_query)

        hits = result.get('hits', {}).get('hits', [])
        if not hits:
            return

        return [Person(**hit['_source']) for hit in hits]

    async def _get_person_from_storage(self, person_id: str) -> Person | None:
        '''Получение личности из хранилища'''
        try:
            doc = await self.storage.get(index='persons', id=person_id)
        except  Exception:
            return None
        return Person(**doc['_source'])
    

person_service = ServiceManager(PersonService, get_elastic)