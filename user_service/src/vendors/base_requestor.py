import asyncio
import logging
from abc import abstractmethod, ABC
from typing import Literal

from aiohttp_retry import RetryClient, RequestParams, ExponentialRetry

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class IAsyncClientRequester(ABC):

    @abstractmethod
    async def call(self, method: str, url: str) -> dict:
        pass


class BaseRequestor(IAsyncClientRequester):

    def __init__(self, attempts: int = 2, start_timeout: float = .2, max_timeout: float = 2.0,
                 factor: float = .4, wrong_statuses: set[int] = None):
        self.retry_options = ExponentialRetry(attempts, start_timeout, max_timeout, factor,
                                              exceptions={asyncio.exceptions.TimeoutError},
                                              statuses=wrong_statuses)

    @staticmethod
    def get_default_headers() -> dict:
        return {'Accept': 'application/json',
                'Content-Type': 'application/json; charset=UTF-8',
                'Connection': 'Keep-Alive',
                'Accept-Encoding': 'gzip',
                'User-Agent': 'okhttp/3.5.0',
                }

    async def call(self, method: Literal['get', 'post', 'delete', 'patch'], url: str, headers=None,
                   data=None, success_statuses=(200, 201, 204)) -> dict:
        if headers is None:
            headers = self.get_default_headers()

        req_param = RequestParams(method=method, url=url, headers=headers, kwargs={'json': data})

        async with RetryClient(raise_for_status=False, retry_options=self.retry_options) as client:
            async with client.requests(params_list=[req_param]) as resp:
                logger.info("Sending request...")
                logger.debug(
                    f'Request with Method: {req_param.method.upper()} || '
                    f'Url: {req_param.url} || Headers: {req_param.headers} || '
                    f'Data: {data}'
                )
                if resp.status in success_statuses:
                    logger.info("Successfully request finish")
                    response = await resp.json()
                    logger.debug(
                        f'Response: {response}'
                    )
                    return response

                logger.warning(f'Bad response -- Status code: {resp.status} message: {await resp.json()}')
                return {}
