from fastapi.testclient import TestClient
from tests.conftest import BASE_API_URL as URL


def test_list_posts(test_client: TestClient, create_fake_data: int):
    result = test_client.get(URL)
    assert result.status_code == 200
    assert len(result.json()) == 2


def test_list_posts_no_data(test_client: TestClient):
    result = test_client.get(URL)
    assert result.status_code == 200
    assert result.json() == []
