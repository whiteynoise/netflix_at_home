import pytest


@pytest.mark.parametrize(
    "api_path, redis_key",
    [
        ("/api/v1/genres/", "genres_main_"),
        (
            "/api/v1/genres/5a4d46b8-07ba-4d8f-b376-25ed30944094",
            "genres_uuid_5a4d46b8-07ba-4d8f-b376-25ed30944094",
        ),
    ],
)
@pytest.mark.asyncio
async def test_genre_redis(
    # prepare_data_for_es,
    cache_checkout,
    api_path: str,
    redis_key: str,
):
    old_cache, modified_cache, old_response, new_response = await cache_checkout(
        redis_key=redis_key, api_path=api_path, key_to_modify="name"
    )

    assert old_cache == old_response
    assert modified_cache == new_response


@pytest.mark.asyncio
async def test_genre_all(make_get_request):
    api_path: str = "/api/v1/genres/"

    response: dict = await make_get_request(api_path=api_path)

    assert response["status"] == 200
    assert len(response["body"]) == 5


@pytest.mark.parametrize(
    "uuid_genre, status",
    [
        ("5a4d46b8-07ba-4d8f-b376-25ed30944094", 200),
        ("just_some_random_stuff", 404),
        ("0a4dbb6c-1fe6-440b-a9bc-b20b7fc37e6c", 404),
    ],
)
@pytest.mark.asyncio
async def test_genre_specific(make_get_request, uuid_genre: str, status: dict):
    api_path: str = f"/api/v1/genres/{uuid_genre}"

    response: dict = await make_get_request(api_path=api_path)

    assert response["status"] == status
