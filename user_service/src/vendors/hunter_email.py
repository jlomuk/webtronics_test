from typing import Literal

from schemas.hunter_schema import ResponseHunter
from settings import settings
from vendors.base_requester import IAsyncClientRequester, BaseRequester

hunter_checker = None


class HunterRequester:
    REJECT_STATUSES = ('invalid', 'disposable', 'invalid_email')

    def __init__(self, requester: IAsyncClientRequester, api_token: str = settings.HUNTER__API_TOKEN):
        self.requester = requester or BaseRequester()
        self.base_url = "https://api.hunter.io/v2"
        self.api_token = api_token

    async def call(self, method: Literal['get', 'post', 'delete', 'patch'], url: str, success_status: tuple,
                   headers: dict = None,
                   data: dict = None) -> dict:
        if not self.api_token:
            return {}
        return await self.requester.call(method, url, headers, data, success_status)

    async def verify_email(self, email: str) -> bool:
        url = f"{self.base_url}/email-verifier?email={email}&api_key={self.api_token}"
        data = await self.call('get', url, success_status=(200, 400))
        verdict = ResponseHunter(**data)

        if verdict.data and verdict.data.status in self.REJECT_STATUSES:
            return False
        elif verdict.errors and verdict.errors[0].id in self.REJECT_STATUSES:
            return False

        return True


def get_hunter_requester():
    global hunter_checker
    if hunter_checker is None:
        hunter_checker = HunterRequester(BaseRequester(wrong_statuses={202, 222}))
    return hunter_checker
