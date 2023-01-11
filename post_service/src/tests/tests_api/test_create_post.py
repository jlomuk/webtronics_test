import pytest
from fastapi.testclient import TestClient
from tests.conftest import BASE_API_URL as URL

URL = URL + '/'


@pytest.mark.parametrize(
    "title, body, user_id, email, expected_status", [
        ('title1', 'body1', 1, 'email@mail.ru', 201),
        ('title2', 'body2', 1, 'email', 422),
        ('title3', 'body3', None, 'email@mail.ru', 422),
        ('title4', '', 1, 'email@mail.ru', 201),
        ('', 'body3', 1, 'email@mail.ru', 422),
    ],
)
def test_create_post(title, body, user_id, email, expected_status, test_client: TestClient):
    data = {'title': title, 'body': body, 'user_id': user_id, 'email': email}

    result = test_client.post(URL, json=data)
    assert result.status_code == expected_status
