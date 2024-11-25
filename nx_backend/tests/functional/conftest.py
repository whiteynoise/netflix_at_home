import asyncio
import uuid
import pytest_asyncio

from aiohttp import ClientSession
from redis.asyncio import Redis
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from functional.testdata.es_indexes import base_index_settings, index_by_name
from functional.settings import ES_CONFIG, REDIS_CONFIG, URL_APP


@pytest_asyncio.fixture(scope='session')
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name='aiohttp_session', scope='session')
async def aiohttp_session():
    session = ClientSession()
    yield session
    await session.close()


@pytest_asyncio.fixture(name='es_client', scope='session')
async def es_client():
    es_client = AsyncElasticsearch(
        hosts=['{host}:{port}'.format(**ES_CONFIG)],
        verify_certs=False
    )
    yield es_client
    await es_client.close()


@pytest_asyncio.fixture(name='redis_client', scope='session')
async def redis_client():
    redis_client = Redis(**REDIS_CONFIG)
    yield redis_client
    await redis_client.aclose()


@pytest_asyncio.fixture(name='es_write_data')
def es_write_data(es_client: AsyncElasticsearch):
    async def inner(data: list[dict], index_name: str) -> None:

        if await es_client.indices.exists(index=index_name):
            await es_client.indices.delete(index=index_name)

        await es_client.indices.create(
            index=index_name,
            settings=base_index_settings,
            mappings=index_by_name[index_name]
        )

        success, failed = await async_bulk(
            client=es_client,
            actions=data,
            index=index_name,
            stats_only=True,
            refresh=True
        )

        if failed:
            raise Exception('Ошибка записи данных в Elasticsearch')
        
    return inner


@pytest_asyncio.fixture(name='make_get_request')
def make_get_request(aiohttp_session: ClientSession):
    async def inner(api_path: str, params: dict) -> dict:
        response_dict = {}
        url = URL_APP + api_path

        async with aiohttp_session.get(url, params=params) as response:
            response_dict['body'] = await response.json()
            response_dict['headers'] = response.headers
            response_dict['status'] = response.status

        return response_dict

    return inner


@pytest_asyncio.fixture(name='get_test_cache')
def get_test_cache(redis_client: Redis):
    async def inner(redis_key) -> bytes:
        data = await redis_client.get(redis_key)
        await redis_client.delete(redis_key)
        return data
    
    return inner


@pytest_asyncio.fixture(name='film_search_es_data')
def film_search_es_data() -> list[dict]:
    # TODO: доработать потом фикстуру под нужды теста
    es_data = []

    for _ in range(10):
        film_id = str(uuid.uuid4())
        es_data.append(
            {
                '_id': film_id,
                'id': film_id,
                'imdb_rating': 8.5,
                'genres': ['Action', 'Sci-Fi'],
                'title': 'The Star',
                'description': 'New World',
                'directors_names': ['Stan'],
                'actors_names': ['Ann', 'Bob'],
                'writers_names': ['Ben', 'Howard'],
                'directors': [
                    {
                        'id': 'dc12b8fc-3c82-4d31-ad8e-72b69f4e3f95',
                        'name': 'Stan'
                    }
                ],
                'actors': [
                    {
                        'id': 'ef86b8ff-3c82-4d31-ad8e-72b69f4e3f95',
                        'name': 'Ann'
                    },
                    {
                        'id': 'fb111f22-121e-44a7-b78f-b19191810fbf',
                        'name': 'Bob'
                    }
                ],
                'writers': [
                    {
                        'id': 'caf76c67-c0fe-477e-8766-3ab3ff2574b5',
                        'name': 'Ben'
                    },
                    {
                        'id': 'b45bd7bc-2e16-46d5-b125-983d356768c6',
                        'name': 'Howard'
                    }
                ]
            }
        )
    
    return es_data
