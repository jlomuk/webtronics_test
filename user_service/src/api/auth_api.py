from fastapi.exceptions import HTTPException

from fastapi import APIRouter, Depends

from schemas import token_schema as token_schemas, user_schema, auth_schema
from starlette import status

from services.user_service import create_user, get_user_by_email
from services.auth_service import WrongPassword, ExpiredToken, NotValidToken, AuthService
from db.user_model import get_db
from vendors.hunter_email import get_hunter_requester

auth_router = APIRouter(prefix='/auth', tags=['auth'])


@auth_router.post("/refresh_token",
                  description='Обновление access токена',
                  response_model=token_schemas.TokenResponse,
                  status_code=status.HTTP_200_OK)
async def refresh_token(token: token_schemas.RefreshTokenRequest, auth_service: AuthService = Depends(AuthService)):
    try:
        user = auth_service.validate_token(token.refresh_token, is_refresh=True)
        return auth_service.create_jwt_tokens(user)
    except (NotValidToken, ExpiredToken) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)


@auth_router.post("/login",
                  description='Логин пользователя с получением токенов',
                  response_model=token_schemas.TokenResponse,
                  status_code=status.HTTP_200_OK)
async def login(user_request: auth_schema.LoginRequest, auth_service: AuthService = Depends(AuthService),
                db=Depends(get_db)):
    try:
        user = await get_user_by_email(user_request.email, db)
        if auth_service.verify_password(user_request.password, user.password):
            return auth_service.create_jwt_tokens(user)
    except WrongPassword as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=e.detail)


@auth_router.post("/registration",
                  description='Регистрация нового пользователя',
                  response_model=token_schemas.TokenResponse,
                  status_code=status.HTTP_201_CREATED)
async def registration(new_user: auth_schema.RegistrationRequest, auth_service: AuthService = Depends(AuthService),
                       db=Depends(get_db), hunter_checker=Depends(get_hunter_requester)):
    user = await create_user(new_user.dict(), db, hunter_checker)
    return auth_service.create_jwt_tokens(user)


@auth_router.post("/check_token",
                  description='Валидация токена',
                  response_model=user_schema.User,
                  status_code=status.HTTP_200_OK)
async def check_token(token: token_schemas.AccessToken, auth_service: AuthService = Depends(AuthService)):
    try:
        user = auth_service.validate_token(token.access_token)
        return user
    except (NotValidToken, ExpiredToken) as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=e.detail)
