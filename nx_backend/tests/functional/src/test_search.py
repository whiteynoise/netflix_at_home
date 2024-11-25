import pytest
import json


@pytest.mark.parametrize(
    'test_params, expected_answer',
    [
        (
            {
                'request_params': {'query': 'The Star'},
                'redis_key': 'movies_search_thestar_1_50'
            },
            {
                'status': 200, 'length': 10
            }
        ),
        (
            {
                'request_params': {'page_size': 3},
                'redis_key': 'movies_search_1_3'
            },
            {
                'status': 200, 'length': 3
            }
        ),
    ]
)
@pytest.mark.asyncio
async def test_film_search(
    make_get_request,
    es_write_data,
    get_test_cache,
    film_search_es_data: list[dict],
    test_params: dict,
    expected_answer: dict,
):
    # TODO: дописать тест
    await es_write_data(film_search_es_data, 'movies')

    og_response: dict = await make_get_request(
        api_path='/api/v1/films/search/',
        params=test_params['request_params']
    )

    assert og_response['status'] == expected_answer['status']
    assert len(og_response['body']) == expected_answer['length']

    cached_data: bytes = await get_test_cache(
        redis_key=test_params['redis_key']
    )

    # изменить данные в es, затем дернуть апи и сравнить результат с кэшем (?)
    assert cached_data == json.dumps(og_response['body']).encode('utf-8')
