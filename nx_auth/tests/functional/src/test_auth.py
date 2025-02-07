import pytest


@pytest.mark.parametrize(
    'user_data, expected_status',
    [
        (
                {'email': 'user@example.com',
                 'password': 'securepass',
                 'first_name': 'first_name',
                 'last_name': 'last_name',
                 'username': 'username_666'
                 },
                200
        ),

        (
                {'email': 'test@example.com',
                 'password': 'securepass',
                 'first_name': 'strin1g',
                 'last_name': 'string1',
                 'username': 'username666'
                 },
                409
        ),
    ]
)
@pytest.mark.asyncio
async def test_register_user(make_post_request, user_data, expected_status):
    response = await make_post_request('/register', user_data)
    assert response['status'] == expected_status


@pytest.mark.parametrize(
    'user_data, expected_status, access_in_body',
    [
        ({
            'username': 'yamle',
            'email': 'yamle@google.com',
            'password': '1234567910'
        }, 200, True),
        ({
            'username': 'yamle',
            'email': 'yamle@google.com',
            'password': 'wrongpass'
        }, 422, False),
        ({
             'username': 'wrong',
             'email': 'wrong@example.com',
             'password': 'wrong'
         }, 404, False)
    ]
)
@pytest.mark.asyncio
async def test_login(
        db_session_with_data,
        make_post_request,
        user_data,
        expected_status,
        access_in_body: bool
):
    response = await make_post_request('/login', user_data)

    assert response['status'] == expected_status
    assert ('access_token' in response["body"]) == access_in_body


@pytest.mark.parametrize(
    'user_data, expected_status',
    [
        ({
            'email': 'yamle@google.com',
            'password': '1234567910'
        }, 200),
        ({
            'email': 'yamle@google.com',
            'password': 'wrongpass'
        }, 422,),
        ({
             'email': 'wrong@wrong123.com',
             'password': 'wrong'
         }, 404)
    ]
)
@pytest.mark.asyncio
async def test_extra_login_success(db_session_with_data, make_post_request, user_data, expected_status):
    response = await make_post_request('/extra_login', user_data)

    assert response['status'] == expected_status
    assert response['body']['email'] == user_data["email"]


@pytest.mark.parametrize(
    'user_data, expected_status, access_in_body',
    [
        ({
            'username': 'yamle',
            'email': 'yamle@google.com',
            'password': '1234567910'
        }, 200, True),
        ({
            'username': 'yamle',
            'email': 'yamle@google.com',
            'password': 'wrongpass'
        }, 422, False),
        ({
             'username': 'wrong',
             'email': 'wrong@example.com',
             'password': 'wrong'
         }, 404, False)
    ]
)
@pytest.mark.asyncio
async def test_change_user_info(
        db_session_with_data,
        make_post_request,
        make_patch_request,
        user_data,
        expected_status,
        access_in_body: bool
):
    login_response = await make_post_request('/login', user_data)
    access_token = login_response['body']['access_token']

    headers = {'Authorization': f' {access_token}'}

    response = await make_patch_request('/change_user/1',
                                        {'username': 'newusername'}, headers=headers
                                        )
    assert response['status'] == expected_status
    assert ('access_token' in response['body']) == access_in_body
