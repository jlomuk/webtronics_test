import asyncio
import re
from unittest.mock import patch, AsyncMock

import pytest
import pytest_asyncio
from sqlalchemy import insert, text
from asyncpg.exceptions import InvalidCatalogNameError
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine
from sqlalchemy.pool import NullPool
from app import app
from db.connection import get_engine
from db.models import meta
from fastapi.testclient import TestClient
from .fakes import FakeRedisCacheClient

from settings import settings

TEST_URL_DB = f"{settings.POSTGRES_URL}_test"
BASE_API_URL = '/api/v1/post'

engine: AsyncEngine = create_async_engine(TEST_URL_DB + '?prepared_statement_cache_size=0', future=True,
                                          poolclass=NullPool)


async def create_db_if_not_exist():
    try:
        async with engine.connect():
            pass

    except InvalidCatalogNameError:
        db_name = re.search(r'^\W*(postgresql\S+)/(\w+)\W*', TEST_URL_DB).group(2)
        temp_engine = create_async_engine(settings.POSTGRES_URL)
        async with temp_engine.connect() as conn:
            await conn.execute(text("COMMIT"))
            await conn.execute(text(f"CREATE DATABASE {db_name}"))


async def connect_test_db() -> AsyncEngine:
    app.dependency_overrides[get_engine] = lambda: engine
    await create_db_if_not_exist()

    async with engine.begin() as conn:
        await conn.run_sync(meta.create_all)

    return engine


@pytest.fixture(autouse=True)
def mocked_redis_cache():
    with patch('services.post.RedisCacheClient', return_value=FakeRedisCacheClient()) as mocked_redis:
        yield mocked_redis


async def disconnect_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(meta.drop_all)


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def preparing_for_test():
    await connect_test_db()
    yield
    await disconnect_test_db()


@pytest_asyncio.fixture(autouse=True)
async def clear_table():
    for table in meta.tables:
        async with engine.connect() as conn:
            await conn.execute(text("COMMIT"))
            await conn.execute(text(f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE"))


@pytest.fixture(scope='session')
def test_client():
    with TestClient(app) as client:
        yield client


@pytest_asyncio.fixture()
async def create_fake_data() -> int:
    user_id = 1
    async with engine.begin() as conn:
        statement_reaction = insert(meta.tables['post'])
        data = [
            {'title': 'Title1', 'body': "Body1", 'user_id': user_id, 'email': 'TestUser1@mail.ru'},
            {'title': 'Title2', 'body': "Body2", 'user_id': 0, 'email': 'TestUser2@mail.ru'},
        ]
        await conn.execute(statement_reaction, data)

        statement_reaction = insert(meta.tables['reaction'])
        data = [
            {'like': None, 'user_id': 777, 'post_id': 1},
            {'like': None, 'user_id': 778, 'post_id': 2},
        ]
        await conn.execute(statement_reaction, data)
    return user_id
