from fastapi import APIRouter, Response

from schemas import auth
from starlette import status
from settings import settings
from helpers import request

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post("/refresh_token",
                  description='Обновление access токена',
                  responses={200: {"model": auth.TokenResponse}},
                  status_code=status.HTTP_200_OK)
async def refresh_token(token: auth.RefreshTokenRequest):
    url = settings.USER_BACKEND_SERVICE.rstrip('/') + '/auth/refresh_token'
    result = await request.request(url, 'post', data=token.dict())
    return Response(content=result.content, media_type="application/json", status_code=result.status_code)


@auth_router.post("/login",
                  description='Логин пользователя с получением токенов',
                  responses={200: {"model": auth.TokenResponse}},
                  status_code=status.HTTP_200_OK)
async def login(user: auth.LoginRequest):
    url = settings.USER_BACKEND_SERVICE.rstrip('/') + '/auth/login'
    result = await request.request(url, 'post', data=user.dict())
    return Response(content=result.content, media_type="application/json", status_code=result.status_code)


@auth_router.post("/registration",
                  description='Регистрация нового пользователя',
                  responses={200: {"model": auth.TokenResponse}},
                  status_code=status.HTTP_200_OK)
async def registration(new_user: auth.RegistrationRequest):
    url = settings.USER_BACKEND_SERVICE.rstrip('/') + '/auth/registration'
    result = await request.request(url, 'post', data=new_user.dict())
    return Response(content=result.content, media_type="application/json", status_code=result.status_code)
