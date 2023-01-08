from fastapi import Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from helpers.request import request
from settings import settings
from schemas.auth import User
from starlette import status
from schemas.auth import AccessToken


async def auth_wrapper(auth: HTTPAuthorizationCredentials = Security(HTTPBearer())) -> User:
    url = settings.USER_BACKEND_SERVICE.rstrip('/') + '/auth/check_token'
    result = await request(url, method='post', data=AccessToken(access_token=auth.credentials).dict())
    match result.status_code:
        case 200:
            return User(**result.json())
        case 500:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail='Сервис недоступен')
        case _:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')