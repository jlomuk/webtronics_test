from fastapi.testclient import TestClient
from tests.conftest import BASE_API_URL as URL


def test_delete_correct_post(test_client: TestClient, create_fake_data: int):
    user_id, post_id = create_fake_data, 1
    result = test_client.delete(f'{URL}/{post_id}', params={'user_id': user_id})
    assert result.status_code == 204

    check_response = test_client.get(f'{URL}')
    assert len(check_response.json()) == 1


def test_delete_correct_post_without_user(test_client: TestClient, create_fake_data: int):
    user_id, post_id = create_fake_data, 1
    result = test_client.delete(f'{URL}/{post_id}')
    assert result.status_code == 422


def test_delete_not_correct_post(test_client: TestClient, create_fake_data: int):
    user_id = create_fake_data
    result = test_client.delete(f'{URL}/{-1}', params={'user_id': user_id})
    assert result.status_code == 404


def test_delete_correct_post_another_user(test_client: TestClient, create_fake_data: int):
    user_id = -1
    result = test_client.delete(f'{URL}/{1}', params={'user_id': user_id})
    assert result.status_code == 404
