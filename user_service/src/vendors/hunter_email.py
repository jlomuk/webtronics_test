import dataclasses

from vendors.base_requestor import IAsyncClientRequester, BaseRequestor
from settings import settings


@dataclasses.dataclass(init=False)
class ResponseHunter:
    status: str
    email: str

    def __init__(self, **kwargs):
        names = set([f.name for f in dataclasses.fields(self)])
        for k, v in kwargs.items():
            if k in names:
                setattr(self, k, v)


class HunterRequestor:
    REJECT_STATUSES = ('invalid', 'disposable')

    def __init__(self, requestor: IAsyncClientRequester, api_token: str = settings.HUNTER__API_TOKEN):
        self.requestor = requestor or BaseRequestor()
        self.api_token = api_token

    async def call(self, url) -> dict:
        if not self.api_token:
            return {}
        return await self.requestor.call(url)

    async def verify_email(self, email: str) -> bool:
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={self.api_token}"
        data = await self.call(url)
        try:
            verdict = ResponseHunter(**data['data'])
        except (TypeError, KeyError):
            return True

        if verdict.status in self.REJECT_STATUSES:
            return False
        return True


hunter_requestor = HunterRequestor(BaseRequestor(wrong_statuses={202, 222}))
