import pytest


@pytest.mark.parametrize(
    "user_data, expected_status",
    [
        (
            {
                "review_id": "1337a059-24ba-4781-a814-5f07c075e161",
                "action": True,
            },
            404,
        ),
    ],
)
@pytest.mark.asyncio
async def test_create_like(
        make_post_request,
        user_data,
        expected_status,
):
    response = await make_post_request("api/v1/likes/create_like", user_data)
    assert response["status"] == expected_status


@pytest.mark.parametrize(
    "user_data, expected_status",
    [
        (
            {"review_id": "1337a059-24ba-4781-a814-5f07c999e161"}, 404,
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_like(
        make_delete_request,
        user_data,
        expected_status,
):
    response = await make_delete_request(f"api/v1/likes/delete_like/{user_data['review_id']}")
    assert response == expected_status
