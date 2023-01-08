from pydantic import BaseModel, EmailStr
from pydantic.fields import Field


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


class TokenResponse(AccessToken, RefreshTokenRequest):
    pass


# ===============================================================================


class AuthBase(BaseModel):
    email: EmailStr
    password: str


class LoginRequest(AuthBase):
    pass


class RegistrationRequest(AuthBase):
    password_repeat: str


class User(BaseModel):
    id: int
    email: EmailStr
    password: str = Field(None, exclude=True)
