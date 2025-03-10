from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "api_path, redis_key, key_to_modify",
    [
        (
            "/api/v1/persons/a5232057-cf81-47ca-9e46-5ccf27300678",
            "persons_uuid_a5232057-cf81-47ca-9e46-5ccf27300678",
            "name",
        ),
        ("/api/v1/persons/search/", "persons_search_1_50", "name"),
        (
            "/api/v1/persons/a5232057-cf81-47ca-9e46-5ccf27300678/film/",
            "persons_film_a5232057-cf81-47ca-9e46-5ccf27300678",
            "title",
        ),
    ],
)
@pytest.mark.asyncio
async def test_persons_redis(
    cache_checkout, api_path: str, redis_key: str, key_to_modify: str
):
    old_cache, modified_cache, old_response, new_response = await cache_checkout(
        redis_key=redis_key, api_path=api_path, key_to_modify=key_to_modify
    )

    assert old_cache == old_response
    assert modified_cache == new_response


@pytest.mark.parametrize(
    "uuid_person, status",
    [
        ("a5232057-cf81-47ca-9e46-5ccf27300678", HTTPStatus.OK),
        ("just_some_random_stuff", HTTPStatus.NOT_FOUND),
        ("0a4dbb6c-1fe6-440b-a9bc-b20b7fc37e6c", HTTPStatus.NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_persons_specific(make_get_request, uuid_person: str, status: dict):
    api_path: str = f"/api/v1/persons/{uuid_person}"

    response: dict = await make_get_request(api_path=api_path)

    assert response["status"] == status


@pytest.mark.parametrize(
    "uuid_person, status",
    [
        ("a5232057-cf81-47ca-9e46-5ccf27300678", HTTPStatus.OK),
        ("just_some_random_stuff", HTTPStatus.NOT_FOUND),
        ("0a4dbb6c-1fe6-440b-a9bc-b20b7fc37e6c", HTTPStatus.NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_persons_films_specific(make_get_request, uuid_person: str, status: dict):
    api_path: str = f"/api/v1/persons/{uuid_person}/film/"

    response: dict = await make_get_request(api_path=api_path)

    assert response["status"] == status


@pytest.mark.parametrize(
    "test_params, expected_answer",
    [
        (
            {"query": "Elizabeth"},
            {"status": HTTPStatus.OK, "length": 5},
        ),
        (
            {"page_size": 3},
            {"status": HTTPStatus.OK, "length": 3},
        ),
        (
            {"query": "Tommy Wiseau"},
            {"status": HTTPStatus.NOT_FOUND, "length": 1},
        ),
        (
            {"page_size": 100, "page_number": 2},
            {"status": HTTPStatus.NOT_FOUND, "length": 1},
        ),
        (
            {},
            {"status": HTTPStatus.OK, "length": 5},
        ),
    ],
)
@pytest.mark.asyncio
async def test_persons_search(
    make_get_request, test_params: dict, expected_answer: dict
):
    api_path: str = "/api/v1/persons/search/"
    request_params: dict = test_params

    response: dict = await make_get_request(api_path=api_path, params=request_params)

    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]
