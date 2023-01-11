from aiocache import caches
from aiocache import RedisCache

from aiocache.serializers import JsonSerializer, BaseSerializer

import settings


class RedisCacheClient:

    def __init__(self, host: str = settings.settings.REDIS_HOST, port: str = settings.settings.REDIS_PORT,
                 timeout: int = 1, serializer: BaseSerializer = JsonSerializer):
        self.host = host
        self.port = port
        self.timeout = timeout
        self.serializer = serializer
        caches.set_config(self.config())
        self.cache: RedisCache = caches.get('default')

    def config(self):
        return {
            'default': {
                'cache': "aiocache.RedisCache",
                'endpoint': self.host,
                'port': self.port,
                'timeout': self.timeout,
                'serializer': {
                    'class': self.serializer
                },
                'plugins': []
            }
        }

    async def get(self, key: str) -> dict | list | str:
        return await self.cache.get(key)

    async def set(self, key: str, value: dict | list | str):
        return await self.cache.set(key, value)

    async def exists(self, key: str):
        return await self.cache.exists(key)
