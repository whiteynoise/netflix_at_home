from http import HTTPStatus

import pytest


@pytest.mark.parametrize(
    "api_path, redis_key",
    [
        (
            "/api/v1/films/search/",
            "movies_search_1_50",
        ),
        ("/api/v1/films/", "movies_main_1_50_-imdb_rating"),
        (
            "/api/v1/films/d7bfb1fb-3157-4beb-a58a-7a58daa01845",
            "movies_uuid_d7bfb1fb-3157-4beb-a58a-7a58daa01845",
        ),
    ],
)
@pytest.mark.asyncio
async def test_film_redis(
    cache_checkout,
    api_path: str,
    redis_key: str,
):
    old_cache, modified_cache, old_response, new_response = await cache_checkout(
        redis_key=redis_key, api_path=api_path, key_to_modify="title"
    )

    assert old_cache == old_response
    assert modified_cache == new_response


@pytest.mark.asyncio
async def test_film_all(make_get_request):
    api_path: str = "/api/v1/films/"

    response: dict = await make_get_request(api_path=api_path)

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == 5

    response: dict = await make_get_request(
        api_path=api_path, params={"genre": "Sci-Fi"}
    )

    assert response["status"] == HTTPStatus.OK
    assert len(response["body"]) == 5


@pytest.mark.parametrize(
    "uuid_film, status",
    [
        ("d7bfb1fb-3157-4beb-a58a-7a58daa01845", HTTPStatus.OK),
        ("just_some_random_stuff", HTTPStatus.NOT_FOUND),
        (1, HTTPStatus.NOT_FOUND),
    ],
)
@pytest.mark.asyncio
async def test_film_specific(make_get_request, uuid_film: str, status: dict):
    api_path: str = f"/api/v1/films/{uuid_film}"

    response: dict = await make_get_request(api_path=api_path)

    assert response["status"] == status


@pytest.mark.parametrize(
    "test_params, expected_answer",
    [
        (
            {"query": "The Star"},
            {"status": HTTPStatus.OK, "length": 5},
        ),
        (
            {"page_size": 3},
            {"status": HTTPStatus.OK, "length": 3},
        ),
        (
            {"query": "SomeFunnyStaff"},
            {"status": HTTPStatus.NOT_FOUND, "length": 1},
        ),
        (
            {"page_size": 100, "page_number": 2},
            {"status": HTTPStatus.NOT_FOUND, "length": 1},
        ),
    ],
)
@pytest.mark.asyncio
async def test_film_search(
    make_get_request,
    test_params: dict,
    expected_answer: dict,
):
    api_path: str = "/api/v1/films/search/"
    request_params: dict = test_params

    response: dict = await make_get_request(api_path=api_path, params=request_params)

    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]
