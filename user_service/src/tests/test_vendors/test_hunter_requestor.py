import pytest


@pytest.mark.parametrize(
    "email, expected",
    [
        ("valid@email.ru", True),
        ("invalid@email.ru", False),
        ("disposable@emal.ru", False),
        ("unknown@email.ru", True),
    ]
)
@pytest.mark.asyncio
async def test_verify_email(email, expected, instance_hunter):
    res: bool = await instance_hunter.verify_email(email)
    assert res == expected


@pytest.mark.parametrize(
    "email, expected",
    [
        ("valid@email.ru", True),
        ("invalid@email.ru", True),
        ("disposable@emal.ru", True),
    ]
)
@pytest.mark.asyncio
async def test_without_api_token_verify_email(email, expected, instance_hunter_disabled):
    res: bool = await instance_hunter_disabled.verify_email(email)
    assert res == expected
