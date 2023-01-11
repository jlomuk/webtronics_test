import pytest
from fastapi.testclient import TestClient
from tests.conftest import BASE_API_URL as URL


@pytest.mark.parametrize(
    "post_id, expected_status, expected_data",
    [
        (1, 200, 'reaction'),
        (2222, 404, 'detail'),
        ('key', 422, 'detail')
    ],
)
def test_get_post(post_id, expected_status, expected_data, test_client: TestClient, create_fake_data: int):
    result = test_client.get(f'{URL}/{post_id}')
    assert result.status_code == expected_status
    assert expected_data in result.json()
