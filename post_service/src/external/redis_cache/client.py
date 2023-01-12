# from aiocache import caches
# from aiocache import RedisCache
# from aiocache.base import SENTINEL
#
# from aiocache.serializers import JsonSerializer, BaseSerializer
import json

import aioredis

import settings


class RedisCacheClient:

    def __init__(self, host: str = settings.settings.REDIS_HOST, port: str = settings.settings.REDIS_PORT):
        self.host = host
        self.port = port
        self.cache: aioredis.Redis = aioredis.from_url(f'redis://{self.host}:{self.port}', decode_responses=True)

    async def get(self, key: str) -> dict | list | str:
        value = await self.cache.get(key)
        if value:
            return json.loads(value)

    async def set(self, key: str, value: dict | list | str) -> bool:
        return await self.cache.set(key, json.dumps(value))

    async def exists(self, key: str) -> bool:
        return await self.cache.exists(key)
