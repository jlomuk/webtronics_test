import json
from typing import Any

import aioredis

import settings


class RedisCacheClient:

    def __init__(self, host: str = settings.settings.REDIS_HOST, port: str = settings.settings.REDIS_PORT,
                 db: str = '0'):
        self.host = host
        self.port = port
        self.db = db
        self.cache: aioredis.Redis = aioredis.from_url(f'redis://{self.host}:{self.port}/{self.db}',
                                                       decode_responses=True)
        self.pipeline = None

    async def get(self, key: str) -> dict | list | str:
        value = await self.cache.get(key)
        if value:
            return json.loads(value)

    async def set(self, key: str, value: dict | list | str) -> bool:
        return await self.cache.set(key, json.dumps(value))

    def set_pipeline(self):
        self.pipeline = self.cache.pipeline()

    def pset(self, key: str, value: dict | list | str):
        if self.pipeline is None:
            self.set_pipeline()
        return self.pipeline.set(key, json.dumps(value))

    def pget(self, key: str):
        if self.pipeline is None:
            self.set_pipeline()
        return self.pipeline.get(key)

    async def execute_pipeline(self) -> list[Any]:
        result = await self.pipeline.execute()
        await self.close_pipeline()
        return [json.loads(value) if isinstance(value, (str, bytes, bytearray)) else value for value in result]

    async def close_pipeline(self):
        self.pipeline = None
