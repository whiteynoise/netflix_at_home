from db.elastic import get_elastic
from models.response_models import FilmWork
from services.abstract_models import ServiceManager, Storage
from services.utils.paginator_ import get_offset

from nx_content.src.models.entity_models import SimpleFilmWork


class FilmService:
    def __init__(self, storage: Storage):
        self.storage = storage

    async def get_by_id(self, film_id: str) -> FilmWork | None:
        """Получение кинопроизведения по id"""
        film = await self._get_film_from_storage(film_id)

        if not film:
            return None

        return film

    async def search_films(
        self, get_query: str | None, page_number: int, page_size: int
    ) -> list[FilmWork] | None:
        """Поиск фильмов в хранилище с поддержкой пагинации."""

        offset = get_offset(page_number, page_size)

        search_query = {
            "from": offset,
            "size": page_size,
        }

        if get_query:
            search_query["query"] = {
                "bool": {"must": [{"match": {"title": get_query}}]}
            }

        result = await self.storage.search(index="movies", body=search_query)

        hits = result.get("hits", {}).get("hits", [])

        if not hits:
            return None

        return [FilmWork(**hit["_source"]) for hit in hits]

    async def sorted_films(
        self,
        sort: str,
        genre: str | None,
        page_number: int,
        page_size: int,
    ) -> list[FilmWork] | None:
        """Отдает фильмы посорченные по заданному полю и отфильтрованные по жанрам"""

        sort_order = "desc" if sort[0] == "-" else "asc"
        sort = sort.lstrip("-")

        offset = get_offset(page_number, page_size)

        search_query = {
            "from": offset,
            "size": page_size,
            "sort": [{sort: {"order": sort_order}}],
            "query": {"bool": {"must": [], "filter": []}},
        }

        if genre:
            search_query["query"]["bool"]["filter"].append({"term": {"genres": genre}})

        result = await self.storage.search(index="movies", body=search_query)

        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            return None

        return [FilmWork(**hit["_source"]) for hit in hits]

    async def _get_films_by_person(self, person_id: int) -> list[FilmWork] | None:
        """Возращает найденные фильмы по личности"""
        search_query = {
            "query": {
                "bool": {
                    "should": [
                        {
                            "nested": {
                                "path": "directors",
                                "query": {"term": {"directors.id": person_id}},
                            }
                        },
                        {
                            "nested": {
                                "path": "actors",
                                "query": {"term": {"actors.id": person_id}},
                            }
                        },
                        {
                            "nested": {
                                "path": "writers",
                                "query": {"term": {"writers.id": person_id}},
                            }
                        },
                    ]
                }
            }
        }
        result = await self.storage.search(index="movies", body=search_query)
        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            return None

        return [FilmWork(**hit["_source"]) for hit in hits]

    async def _get_film_from_storage(self, film_id: str) -> FilmWork | None:
        """Получение кинопроизведения из хранилища"""
        try:
            doc = await self.storage.get(index="movies", id=film_id)
        except Exception:
            return None
        return FilmWork(**doc["_source"])

    async def get_films_by_ids(self, film_ids: list[str]) -> list[FilmWork]:
        """Получение списка фильмов по списку ID"""
        search_query = {
            "query": {"bool": {"filter": [{"terms": {"id": film_ids}}]}},
            "size": len(film_ids),
        }

        result = await self.storage.search(index="movies", body=search_query)
        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            return []

        return [
            SimpleFilmWork(
                id=hit["_source"]["id"],
                imdb_rating=hit["_source"]["imdb_rating"],
                title=hit["_source"]["title"],
            )
            for hit in hits
        ]


film_service = ServiceManager(FilmService, get_elastic)
