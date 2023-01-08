import httpx
import typing as t

JSONValue = t.Union[str, int, float, bool, None, t.Dict[str, t.Any], t.List[t.Any]]


async def request(url, method, data=None, params=None, custom_headers=None) -> httpx.Response:
    async with httpx.AsyncClient() as client:
        headers = httpx.Headers({
            'content-type': 'application/json'
        })
        if custom_headers:
            headers.update(custom_headers)

        match method:
            case 'get':
                requester = client.get(url=url, params=params, headers=headers)
            case 'post':
                requester = client.post(url=url, json=data, params=params, headers=headers)
            case 'delete':
                requester = client.delete(url=url, params=params, headers=headers)
            case 'patch':
                requester = client.patch(url=url, json=data, params=params, headers=headers)
            case _:
                return httpx.Response(status_code=500, headers=headers, json={'status': 'Метод недоступен'})

        try:
            return await requester
        except:
            return httpx.Response(status_code=500, headers=headers, json={'status': 'Ошибка сервиса'})
