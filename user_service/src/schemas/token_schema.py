from pydantic import BaseModel


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class AccessToken(BaseModel):
    access_token: str


class TokenResponse(AccessToken, RefreshTokenRequest):
    pass
