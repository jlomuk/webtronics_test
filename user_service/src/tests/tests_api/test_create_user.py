from starlette.testclient import TestClient
import pytest

URL = '/api/v1/auth/registration'


def test_registration_user(test_client: TestClient):
    body_reg = {
        'email': 'Test_user1@mail.co',
        'password': 'password666',
        'password_repeat': 'password666'
    }
    res = test_client.post(URL, json=body_reg)
    assert res.status_code == 201
    assert 'access_token' in res.json()


@pytest.mark.parametrize(
    "body, expected_status_code, msg",
    [
        [{'email': 'Test_user1@mail.co', 'password': 'password666', 'password_repeat': 'password66'},
         422, 'Пароли не совпадают'],
        [{'email': 'Test_user1@mail.co', 'password': 'pass', 'password_repeat': 'pass'}, 422,
         'Пароль меньше 8 символов'],
    ]
)
def test_registration_with_wrong_pass(test_client: TestClient, body, expected_status_code, msg):
    res = test_client.post(URL, json=body)
    assert res.status_code == expected_status_code
    assert msg == res.json()['detail'][0]['msg']


def test_registration_with_already_registered_user(test_client: TestClient, create_user_db):
    body_reg = {
        'email': 'Test1@mail.su',
        'password': 'password',
        'password_repeat': 'password'
    }
    result_2 = test_client.post(URL, json=body_reg)
    assert result_2.status_code == 400
    assert 'Такой пользователь уже существует' == result_2.json()['detail']
