from starlette.testclient import TestClient

URL = '/api/v1/auth/refresh_token'


def test_refresh_token(test_client: TestClient, create_token):
    tokens = create_token[0]
    response = test_client.post(URL, json=dict(refresh_token=tokens.get('refresh_token')))
    assert response.status_code == 200
    assert 'access_token' in response.json()


def test_wrong_signature_refresh_token(test_client: TestClient, create_token):
    tokens = create_token[0]
    response = test_client.post(URL, json=dict(refresh_token=tokens.get('refresh_token')[:-5] + 'hfsDk'))
    assert response.status_code == 401
    assert response.json() == {'detail': 'Передан невалидный токен'}


def test_expired_refresh_token(test_client: TestClient, create_invalid_token):
    tokens = create_invalid_token[0]
    response = test_client.post(URL, json=dict(refresh_token=tokens.get('refresh_token')))
    assert response.status_code == 401
    assert response.json() == {'detail': 'Срок действия токена закончился'}
