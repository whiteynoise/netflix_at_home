import pytest


@pytest.mark.parametrize(
    "user_data, expected_status",
    [
        (
            {
                "film_id": "1846a059-24ba-4781-a814-5f07c075e161",
                "review_text": 'Great movie',
                "rating_by_user": 10
            },
            200,
        ),
        (
            {
                "film_id": "1846a059-24ba-4781-a814-5f07c075e161",
                "review_text": 'Not a great movie',
                "rating_by_user": 10
            },
            409,
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_review(
        make_post_request,
        user_data,
        expected_status,
):
    response = await make_post_request("api/v1/reviews/create_review", user_data)
    assert response["status"] == expected_status


@pytest.mark.parametrize(
    "result, expected_status",
    [
        (1, 200),
    ],
)
@pytest.mark.asyncio
async def test_get_my_reviews(
        result,
        make_get_request,
        expected_status,
):
    response = await make_get_request("api/v1/reviews/me", rest_style=True)
    assert response["status"] == expected_status
    assert len(response['body']) == result


@pytest.mark.parametrize(
    "film_id, expected_status",
    [
        ("1846a059-24ba-4781-a814-5f07c075e161", 200),
        ("1337a059-24ba-4781-a814-5f07c075e161", 404),
    ],
)
@pytest.mark.asyncio
async def test_delete_review(
        make_delete_request,
        film_id,
        expected_status,
):
    response = await make_delete_request(f"api/v1/reviews/{film_id}/delete_review")
    assert response == expected_status
