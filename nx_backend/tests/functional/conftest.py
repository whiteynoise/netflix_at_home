import asyncio
import copy
import json
import uuid
import pytest_asyncio

from aiohttp import ClientSession
from redis.asyncio import Redis

from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk

from functional.settings import ES_CONFIG, REDIS_CONFIG, URL_APP
from functional.testdata.es_indexes import base_index_settings, index_by_name
from functional.testdata.base_test_rows import base_row_by_name


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
    async def inner(api_path: str, params: dict = {}) -> dict:
        response_dict = {}
        url = URL_APP + api_path

        async with aiohttp_session.get(url, params=params) as response:
            response_dict['body'] = await response.json()
            response_dict['headers'] = response.headers
            response_dict['status'] = response.status

        return response_dict

    return inner
    

@pytest_asyncio.fixture(name='cache_checkout')
def cache_checkout(
    redis_client: Redis,
    make_get_request
):
    async def inner(
        redis_key: str,
        api_path: str,
        key_to_modify: str,
        request_params: dict = {}
    ):
        # TODO: разделить фикстуру на две (?)
        old_response: dict = await make_get_request(
            api_path=api_path
        )

        if old_response['status'] == 404:
            raise('Записи нет в ES')

        old_body = old_response['body']

        if isinstance(old_body, list):
            modified_cache: dict = copy.deepcopy(old_body[0])
            modified_cache[key_to_modify] = 'SomeRandomRedisTest'
            modified_cache: list[dict] = [modified_cache]
        else:
            modified_cache: dict = copy.deepcopy(old_body)
            modified_cache[key_to_modify] = 'SomeRandomRedisTest'
        
        modified_cache: bytes = json.dumps(modified_cache).encode('utf-8')

        old_cache: bytes = await redis_client.get(name=redis_key)

        await redis_client.set(
            name=redis_key,
            value=modified_cache,
            ex=60 * 5
        )

        new_response: dict = await make_get_request(
            api_path=api_path,
            params=request_params
        )

        await redis_client.delete(redis_key)

        return (
            old_cache,
            modified_cache,
            json.dumps(old_body).encode('utf-8'),
            json.dumps(new_response['body']).encode('utf-8'),
        )
    
    return inner


@pytest_asyncio.fixture(name='prepare_data_for_es')
def prepare_data_for_es(es_write_data):
    async def inner(
        index_name: str,
        len_of_prepared_data: int
    ) -> dict:
        base_row: dict = base_row_by_name[index_name]
        es_data = [base_row]

        for _ in range(len_of_prepared_data - 1):
            data = copy.deepcopy(base_row)
            data['_id'] = str(uuid.uuid4())
            data['id'] = data['_id']
            es_data.append(data)
        
        await es_write_data(
            data=es_data,
            index_name=index_name
        )

    return inner
