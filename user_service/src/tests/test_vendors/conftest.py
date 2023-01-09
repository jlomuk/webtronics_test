from pytest_asyncio import fixture
from urllib.parse import urlparse, parse_qs

from vendors.base_requestor import IAsyncClientRequester
from vendors.hunter_email import HunterRequestor


class MockHunterRequestor(IAsyncClientRequester):
    INNER_TEST_DATA = {
        'valid@email.ru': {
            "data": {
                "status": "valid",
                "result": "deliverable",
                "_deprecation_notice": "Using result is deprecated, use status instead",
                "email": "patrick@stripe.com"}},
        'invalid@email.ru': {
            "data": {
                "status": "invalid",
                "result": "deliverable",
                "_deprecation_notice": "Using result is deprecated, use status instead",
                "email": "patrick@stripe.com"}},
        'disposable@emal.ru': {
            "data": {
                "status": "disposable",
                "result": "deliverable",
                "_deprecation_notice": "Using result is deprecated, use status instead",
                "email": "patrick@stripe.com"}},
        'unknown@email.ru': {
            "data": {
                "status": "unknown",
                "result": "deliverable",
                "_deprecation_notice": "Using result is deprecated, use status instead",
                "email": "patrick@stripe.com"}},
        'webmail@email.ru': {
            "data": {
                "status": "webmail",
                "result": "deliverable",
                "_deprecation_notice": "Using result is deprecated, use status instead",
                "email": "patrick@stripe.com"}},

    }

    async def call(self, url: str) -> dict:
        try:
            email = parse_qs(urlparse(url).query)['email'][0]
            result = self.INNER_TEST_DATA[email]
        except Exception:
            return {}
        else:
            return result


@fixture()
def instance_hunter() -> HunterRequestor:
    return HunterRequestor(MockHunterRequestor(), api_token='test_token')


@fixture()
def instance_hunter_disabled() -> HunterRequestor:
    return HunterRequestor(MockHunterRequestor(), api_token='')
