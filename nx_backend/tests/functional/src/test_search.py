import pytest


@pytest.mark.parametrize(
    "test_params, expected_answer",
    [
        (
            {"query": "The Star"},
            {"status": 200, "length": 5},
        ),
        (
            {"page_size": 3},
            {"status": 200, "length": 3},
        ),
        (
            {"query": "SomeFunnyStaff"},
            {"status": 404, "length": 1},
        ),
        (
            {"page_size": 100, "page_number": 2},
            {"status": 404, "length": 1},
        ),
    ],
)
@pytest.mark.asyncio
async def test_film_search1(
    make_get_request,
    test_params: dict,
    expected_answer: dict,
):
    api_path: str = "/api/v1/films/search/"
    request_params: dict = test_params

    response: dict = await make_get_request(api_path=api_path, params=request_params)

    assert response["status"] == expected_answer["status"]
    assert len(response["body"]) == expected_answer["length"]
