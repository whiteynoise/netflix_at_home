from db.elastic import get_elastic
from models.entity_models import Genres
from services.abstract_models import ServiceManager, Storage


class GenreService:
    def __init__(self, storage: Storage):
        self.storage = storage

    async def get_by_id(self, genre_id: str) -> Genres | None:
        '''Получение информации жанра по id'''
        genre = await self._get_genre_from_storage(genre_id)
        if not genre:
            return
        return genre

    async def get_genres(self) -> list[Genres] | None:
        'Отдает все жанры'
        search_query = {'query': {'match_all': {}}}
        result = await self.storage.search(index='genres', body=search_query)
        hits = result['hits']['hits']
        if not hits:
            return
        genres = [Genres(**hit['_source']) for hit in hits]
        return genres

    async def _get_genre_from_storage(self, genre_id: str) -> Genres | None:
        '''Получение жанра из хранилища'''
        try:
            doc = await self.storage.get(index='genres', id=genre_id)
        except Exception:
            return
        return Genres(**doc['_source'])


genre_service = ServiceManager(GenreService, get_elastic)