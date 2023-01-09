from urllib.parse import parse_qs, urlparse

from vendors.base_requester import IAsyncClientRequester


class MockHunterRequester(IAsyncClientRequester):
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
        'webmail@gmail.c': {
            "errors": [{
                "id": "invalid_email",
                "code": 400}]
        }
    }

    async def call(self, _, url: str, *args, **kwargs) -> dict:
        try:
            email = parse_qs(urlparse(url).query)['email'][0]
            result = self.INNER_TEST_DATA[email]
        except Exception:
            return {}
        else:
            return result
