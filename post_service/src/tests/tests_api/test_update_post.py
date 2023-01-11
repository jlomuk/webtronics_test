import pytest
from fastapi.testclient import TestClient
from tests.conftest import BASE_API_URL as URL

URL = URL


@pytest.mark.parametrize(
    "post_id, title, body, user_id, expected_status, check_field, expected_data", [
        (1, 'title_change', 'body_change', 1, 200, 'title', 'title_change'),  # Корректные данные
        (1, 'title_change', 'body_change', 9999, 404, 'title', 'Title1'),  # Обновляет не owner поста
        (9999, 'title_change', 'body_change', 1, 404, 'detail', 'Пост не найден'),  # Не существующий пост
        (1, 'title_change', '', 1, 200, 'body', ''),  # Обновлeние с пустым телом поста
        (1, '', 'body_change', 1, 422, 'title', 'Title1'),  # Обновлeние с пустым title поста
        (1, '', '', 1, 422, 'title', 'Title1'),  # Обновлeние с пустым title и body поста
        (1, 'title_change', 'body_change', None, 422, 'title', 'Title1'),  # Обновлeние без передачи user_id поста
        (1, None, 'body_change', 1, 200, 'body', 'body_change'),  # Обновлeние без передачи поля title поста
        (1, 'title_change', None, 1, 200, 'title', 'title_change'),  # Обновлeние без передачи поля body поста
        (1, None, None, 1, 200, 'title', 'Title1'),  # Обновлeние без передачи полей и title, и body поста
    ],
)
def test_update_post(title, body, user_id, expected_status, check_field, expected_data, post_id,
                     test_client: TestClient, create_fake_data: int):
    raw_data = {'title': title, 'body': body, 'user_id': user_id}
    data = {key: str(value) for key, value in raw_data.items() if value is not None}

    result = test_client.patch(f'{URL}/{post_id}', json=data)
    assert result.status_code == expected_status

    check_result = test_client.get(f'{URL}/{post_id}').json()
    assert check_result[check_field] == expected_data
