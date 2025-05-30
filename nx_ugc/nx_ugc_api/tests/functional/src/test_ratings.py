import pytest


@pytest.mark.parametrize(
    "user_data, expected_status",
    [
        (
            {
                "film_id": "1846a059-24ba-4781-a814-5f07c075e161",
                "film_name": "The Batman",
                "rating": 7
            },
            201,
        ),
        (
            {
                "film_id": "1846a059-24ba-4781-a814-5f07c075e161",
                "film_name": "The Batman",
                "rating": 7
            },
            409,
        ),
        (
            {
                "film_id": "6be63706-b177-4e2b-9b2f-c0bae5015f10",
                "film_name": "Once Upon a Time... in Hollywood",
                "rating": 12
            },
            422,
        ),
        (
            {
                "film_id": "6be63706-b177-4e2b-9b2f-c0bae5015f10",
                "film_name": "Once Upon a Time... in Hollywood",
                "rating": 10
            },
            200,
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_rating(
        make_post_request,
        user_data,
        expected_status,
):
    response = await make_post_request("api/v1/rating/add_rating", user_data)
    assert response["status"] == expected_status


@pytest.mark.parametrize(
    "user_data, expected_status",
    [
        (
            {
                "film_id": "1846a059-24ba-4781-a814-5f07c075e161",
                "rating": 8
            },
            200,
        ),
        (
            {
                "film_id": "1846a059-24ba-4781-a814-5f07c075e161",
                "rating": 0
            },
            422,
        ),
    ],
)
@pytest.mark.asyncio
async def test_update_rating(
        make_patch_request,
        user_data,
        expected_status,
):
    response = await make_patch_request("api/v1/rating/update_rating", user_data)
    assert response["status"] == expected_status


@pytest.mark.parametrize(
    "user_data, expected_status, result",
    [
        (
            {"film_id": "1846a059-24ba-4781-a814-5f07c075e161"}, 200, 1,
        ),
        (
            {}, 200, 2,
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_rating(
        make_get_request,
        user_data,
        expected_status,
        result,
):
    response = await make_get_request("api/v1/rating/get_rating", user_data)

    assert response["status"] == expected_status
    assert len(response["body"]) == result


@pytest.mark.parametrize(
    "user_data, expected_status, result",
    [
        (
            {"film_id": "1846a059-24ba-4781-a814-5f07c075e161"}, 200, 8,
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_avg_film_rating(
        make_get_request,
        user_data,
        expected_status,
        result,
):
    response = await make_get_request("api/v1/rating/get_avg_film_rating", user_data)

    assert response["status"] == expected_status
    assert response["body"]['avg_rating'] == result
