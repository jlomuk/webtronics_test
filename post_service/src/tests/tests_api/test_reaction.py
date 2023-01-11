import pytest
from fastapi.testclient import TestClient
from tests.conftest import BASE_API_URL as URL


def test_reaction_not_exists_post(test_client: TestClient):
    post_id, user_id = 9999999, 1

    result = test_client.get(f'{URL}/{post_id}/like', params={'user_id': user_id})
    assert result.status_code == 404

    result = test_client.get(f'{URL}/{post_id}/dislike', params={'user_id': user_id})
    assert result.status_code == 404


@pytest.mark.parametrize(
    "post_id, user_id, expected_status, expected_data", [
        (1, 1, 200, 0),  # Не можем ставить лайки своему посту
        (1, 999, 200, 1),  # Можем ставить лайки чужим постам
        (2, 1, 200, 1)
    ],
)
def test_reaction_post(post_id, user_id, expected_status, expected_data, test_client: TestClient,
                       create_fake_data: int):
    result = test_client.get(f'{URL}/{post_id}/like', params={'user_id': user_id})
    assert result.status_code == expected_status
    assert result.json()['reaction']['like'] == expected_data

    result = test_client.get(f'{URL}/{post_id}/dislike', params={'user_id': user_id})
    assert result.status_code == expected_status
    assert result.json()['reaction']['dislike'] == expected_data


def test_correct_counter_likes(test_client: TestClient, create_fake_data):
    post_id = 1
    user_id_1, user_id_2 = 777, 778

    result = test_client.get(f'{URL}/{post_id}').json()
    assert result['reaction']['like'] == 0

    test_client.get(f'{URL}/{post_id}/like', params={'user_id': user_id_1})

    result = test_client.get(f'{URL}/{post_id}').json()
    assert result['reaction']['like'] == 1

    test_client.get(f'{URL}/{post_id}/like', params={'user_id': user_id_2})

    result = test_client.get(f'{URL}/{post_id}').json()
    assert result['reaction']['like'] == 2

    test_client.get(f'{URL}/{post_id}/like', params={'user_id': user_id_1})

    result = test_client.get(f'{URL}/{post_id}').json()
    assert result['reaction']['like'] == 1


def test_correct_change_like_to_dislike(test_client: TestClient, create_fake_data):
    post_id = 1
    user_id = 777

    result = test_client.get(f'{URL}/{post_id}').json()
    assert result['reaction']['like'] == 0
    assert result['reaction']['dislike'] == 0

    test_client.get(f'{URL}/{post_id}/like', params={'user_id': user_id})

    result = test_client.get(f'{URL}/{post_id}').json()
    assert result['reaction']['like'] == 1
    assert result['reaction']['dislike'] == 0

    test_client.get(f'{URL}/{post_id}/dislike', params={'user_id': user_id})

    result = test_client.get(f'{URL}/{post_id}').json()
    assert result['reaction']['like'] == 0
    assert result['reaction']['dislike'] == 1

    test_client.get(f'{URL}/{post_id}/dislike', params={'user_id': user_id})

    result = test_client.get(f'{URL}/{post_id}').json()
    assert result['reaction']['like'] == 0
    assert result['reaction']['dislike'] == 0
