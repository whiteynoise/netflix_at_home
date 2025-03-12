import asyncio

import pytest_asyncio
from aiohttp import ClientSession, TCPConnector

from .settings import URL_APP


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


@pytest_asyncio.fixture(name="auth_token", scope="session", autouse=True)
async def auth_token(aiohttp_session: ClientSession):
    AUTH_SERVICE_URL = 'http://nx_auth:8001/auth-service/api/v1/auth'
    register_url = AUTH_SERVICE_URL + '/register'
    reg_data = {
        "email": "egsy542@example.com",
        "password": "securepass",
        "first_name": "first_name",
        "last_name": "last_name",
        "username": "egsy_lo_542",
    }

    login_url = AUTH_SERVICE_URL + '/login'
    log_data = {
        "username": "egsy_lo_542",
        "email": "egsy542@example.com",
        "password": "securepass"
    }

    async with aiohttp_session.post(register_url, json=reg_data, ssl=False):
        pass

    async with aiohttp_session.post(login_url, json=log_data, ssl=False) as response:
        res = await response.json()

    yield res['access_token']


@pytest_asyncio.fixture(name="auth_header")
async def auth_header(auth_token):
    return {"Authorization": f"{auth_token}"}


@pytest_asyncio.fixture(name="make_get_request")
def make_get_request(aiohttp_session: ClientSession, auth_header):
    async def inner(
            api_path: str,
            params: dict | None = None,
            headers: dict | None = None,
            rest_style: bool = False,
    ) -> dict:
        response_dict = {}
        url = URL_APP + api_path
        headers = headers or auth_header

        params = params or {}
        request_params = {'params': params} if rest_style else {'json': params}

        async with aiohttp_session.get(url, **request_params, headers=headers, ssl=False) as response:
            response_dict["body"] = await response.json()
            response_dict["headers"] = response.headers
            response_dict["status"] = response.status

        return response_dict

    return inner


@pytest_asyncio.fixture(name="make_post_request")
def make_post_request(aiohttp_session: ClientSession, auth_header):
    async def inner(api_path: str, data: dict | None = None, headers=None) -> dict:
        response_dict = {}
        url = URL_APP + api_path
        headers = headers or auth_header

        async with aiohttp_session.post(url, json=data or {}, headers=headers, ssl=False) as response:
            response_dict["body"] = await response.json()
            response_dict["headers"] = response.headers
            response_dict["status"] = response.status

        return response_dict

    return inner


@pytest_asyncio.fixture(name="make_patch_request")
def make_patch_request(aiohttp_session: ClientSession, auth_header):
    async def inner(api_path: str, data: dict | None = None, headers=None) -> dict:
        response_dict = {}
        url = URL_APP + api_path
        headers = headers or auth_header

        async with aiohttp_session.patch(url, json=data or {}, headers=headers, ssl=False) as response:
            response_dict["body"] = await response.json()
            response_dict["headers"] = response.headers
            response_dict["status"] = response.status

        return response_dict

    return inner


@pytest_asyncio.fixture(name="make_delete_request")
def make_delete_request(aiohttp_session: ClientSession, auth_header):
    async def inner(api_path: str, data: dict | None = None, headers=None) -> dict:
        response_status = None
        url = URL_APP + api_path
        headers = headers or auth_header

        async with aiohttp_session.delete(url, params=data or {}, headers=headers, ssl=False) as response:
            response_status = response.status

        return response_status

    return inner
