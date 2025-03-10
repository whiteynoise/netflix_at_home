import asyncio
import copy
import json
import pytest_asyncio

from http import HTTPStatus
from aiohttp import ClientSession, TCPConnector
from redis.asyncio import Redis
from sqlalchemy.orm import sessionmaker


from db.postgres import Base
from models.entity import Users
from .settings import REDIS_CONFIG, URL_APP, dsn
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


@pytest_asyncio.fixture(name="aiohttp_session", scope="session")
async def aiohttp_session():
    conn = TCPConnector()
    session = ClientSession(connector=conn, trust_env=True)
    yield session
    await session.close()


@pytest_asyncio.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(name="redis_client", scope="session")
async def redis_client():
    redis_client = Redis(**REDIS_CONFIG)
    await redis_client.flushall()
    yield redis_client
    await redis_client.aclose()


@pytest_asyncio.fixture(name="db_session", scope="session")
async def db_session():
    engine = create_async_engine(dsn, echo=True, future=True)

    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with async_session() as session:
        yield session

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(name="db_session_with_data", scope="function")
async def db_session_with_data(db_session: AsyncSession):

    test_user = Users(
        email="yamle@google.com",
        username="yamle",
        first_name="Test",
        last_name="User",
        password="1234567910",
    )

    db_session.add(test_user)
    await db_session.commit()
    await db_session.refresh(test_user)

    yield db_session
    await db_session.delete(test_user)
    await db_session.commit()


@pytest_asyncio.fixture(name="make_get_request")
def make_get_request(aiohttp_session: ClientSession):
    async def inner(api_path: str, params: dict | None = None) -> dict:
        response_dict = {}
        url = URL_APP + api_path

        async with aiohttp_session.get(url, params=params or {}, ssl=False) as response:
            response_dict["body"] = await response.json()
            response_dict["headers"] = response.headers
            response_dict["status"] = response.status

        return response_dict

    return inner


@pytest_asyncio.fixture(name="make_post_request")
def make_post_request(aiohttp_session: ClientSession):
    async def inner(api_path: str, data: dict | None = None) -> dict:
        response_dict = {}
        url = URL_APP + api_path

        async with aiohttp_session.post(url, json=data or {}, ssl=False) as response:
            response_dict["body"] = await response.json()
            response_dict["headers"] = response.headers
            response_dict["status"] = response.status

        return response_dict

    return inner


@pytest_asyncio.fixture(name="make_patch_request")
def make_patch_request(aiohttp_session: ClientSession):
    async def inner(api_path: str, data: dict | None = None) -> dict:
        response_dict = {}
        url = URL_APP + api_path

        async with aiohttp_session.patch(url, json=data or {}, ssl=False) as response:
            response_dict["body"] = await response.json()
            response_dict["headers"] = response.headers
            response_dict["status"] = response.status

        return response_dict

    return inner


@pytest_asyncio.fixture(name="cache_login_token")
async def cache_login_token(redis_client: Redis, make_post_request):
    async def inner(user_data: dict, api_path: str):
        response = await make_post_request(api_path, user_data)

        assert response["status"] == 200
        assert "access_token" in response

        # user_id = user_data['username']
        # access_token = response['access_token']
        #
        # redis_key = str(user_id)
        # old_cache = await redis_client.get(redis_key)
        #
        # await redis_client.set(redis_key, access_token, ex=60 * 5)
        #
        # new_cache = await redis_client.get(redis_key)
        #
        # await redis_client.delete(redis_key)
        # return old_cache, access_token, new_cache

    return inner
