import pytest


@pytest.mark.parametrize(
    "user_data, expected_status",
    [
        (
            {
                "bookmark_name": "watch later",
                "film_id": "cc69a799-6070-4a5e-bb9a-c979c97edde5",
                "film_name": "Blade Runner 2049",
            },
            200,
        ),
        (
            {
                "bookmark_name": "watch later",
                "film_id": "13c537b9-d8e9-42ab-9fd0-7698a08a8023",
                "film_name": "Oppenheimer",
            },
            200,
        ),
        (
            {
                "bookmark_name": "watch later",
                "film_id": "cc69a799-6070-4a5e-bb9a-c979c97edde5",
                "film_name": "Blade Runner 2049",
            },
            409,
        ),
        (
            {
                "bookmark_name": "favorite",
                "film_id": "13c537b9-d8e9-42ab-9fd0-7698a08a8023",
                "film_name": "Oppenheimer",
            },
            200,
        ),
        (
            {
                "bookmark_name": "favorite",
                "film_name": "Oppenheimer",
            },
            422,
        ),
        (
            {
                "bookmark_name": "bookmark to delete",
                "film_id": "cc69a799-6070-4a5e-bb9a-c979c97edde5",
                "film_name": "Blade Runner 2049",
            },
            200,
        ),
        (
            {
                "bookmark_name": "bookmark to delete",
                "film_id": "13c537b9-d8e9-42ab-9fd0-7698a08a8023",
                "film_name": "Oppenheimer",
            },
            200,
        ),
    ],
)
@pytest.mark.asyncio
async def test_add_to_bookmark(
        make_post_request,
        user_data,
        expected_status,
):
    response = await make_post_request("api/v1/bookmarks/add_to_bookmark", user_data)
    assert response["status"] == expected_status


@pytest.mark.parametrize(
    "user_data, expected_status, result",
    [
        (
            {"bookmark_name": "watch later"}, 200, 2,
        ),
        (
            {"bookmark_name": "favorite"}, 200, 1,
        ),
        (
            {"bookmark_name": "random random"}, 200, 0,
        ),
    ],
)
@pytest.mark.asyncio
async def test_get_bookmark_info(
        make_get_request,
        user_data,
        expected_status,
        result,
):
    response = await make_get_request("api/v1/bookmarks/get_bookmark_info", user_data)

    assert response["status"] == expected_status
    assert len(response["body"]) == result


@pytest.mark.parametrize(
    "user_data, expected_status",
    [
        (
            {
                "bookmark_name": "bookmark to delete",
                "film_ids": ["13c537b9-d8e9-42ab-9fd0-7698a08a8023", "cc69a799-6070-4a5e-bb9a-c979c97edde5"],
            },
            200,
        ),
        (
            {
                "film_ids": ["13c537b9-d8e9-42ab-9fd0-7698a08a8023", "cc69a799-6070-4a5e-bb9a-c979c97edde5"],
            },
            422,
        ),
        (
            {
                "bookmark_name": "bookmark to delete",
                "film_ids": "13c537b9-d8e9-42ab-9fd0-7698a08a8023",
            },
            422,
        ),
        (
            {
                "bookmark_name": "watch later",
                "film_ids": ["13c537b9-d8e9-42ab-9fd0-7698a08a8023", "cc69a799-6070-4a5e-bb9a-c979c97edde5"],
            },
            200,
        ),
        (
            {
                "bookmark_name": "favorite",
                "film_ids": ["13c537b9-d8e9-42ab-9fd0-7698a08a8023"],
            },
            200,
        ),
    ],
)
@pytest.mark.asyncio
async def test_delete_from_bookmark(
        make_post_request,
        user_data,
        expected_status,
):
    response = await make_post_request("api/v1/bookmarks/delete_from_bookmark", user_data)
    assert response["status"] == expected_status
