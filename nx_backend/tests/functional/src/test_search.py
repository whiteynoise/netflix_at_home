import pytest
import json
import copy


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
    cache_checkout,
    film_search_test_data: list[dict],
    test_params: dict,
    expected_answer: dict,
):
    # TODO: дописать тест
    await es_write_data(
        data=film_search_test_data,
        index_name='movies'
    )

    api_path: str = '/api/v1/films/search/'
    request_params: dict = test_params['request_params']

    og_response: dict = await make_get_request(
        api_path=api_path,
        params=request_params
    )

    assert og_response['status'] == expected_answer['status']
    assert len(og_response['body']) == expected_answer['length']

    modified_cache: dict = copy.deepcopy(og_response['body'][0])
    modified_cache['title'] = 'RedisTest'
    modified_cache: bytes = json.dumps([modified_cache]).encode('utf-8')

    cached_data, modified_cache, new_response = await cache_checkout(
        redis_key=test_params['redis_key'],
        modified_cache=modified_cache,
        api_path=api_path,
        request_params=request_params
    )

    assert cached_data == json.dumps(og_response['body']).encode('utf-8')
    assert modified_cache == new_response
