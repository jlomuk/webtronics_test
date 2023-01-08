from starlette.testclient import TestClient

URL = '/api/v1/auth/check_token'


def test_correct_check_token(test_client: TestClient, create_token):
    tokens, user = create_token[0], create_token[1]
    response = test_client.post(URL, json=dict(access_token=tokens.get('access_token')))
    assert response.status_code == 200
    assert response.json() == user.dict()


def test_correct_wrong_signature_token(test_client: TestClient, create_token):
    tokens, user = create_token[0], create_token[1]
    response = test_client.post(URL, json=dict(access_token=tokens.get('access_token')[:-5] + 'hfsDk'))
    assert response.status_code == 401
    assert response.json() == {'detail': 'Передан невалидный токен'}


def test_check_expired_token(test_client: TestClient, create_invalid_token):
    tokens, user = create_invalid_token[0], create_invalid_token[1]
    response = test_client.post(URL, json=dict(access_token=tokens.get('access_token')))
    assert response.status_code == 401
    assert response.json() == {'detail': 'Срок действия токена закончился'}
