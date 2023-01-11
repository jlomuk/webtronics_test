import datetime

import pytz
from pydantic import BaseModel, EmailStr, validator

from schemas.custom_base_model import CustomBaseModel


# ==================================REQUEST_SCHEMAS======================================

class BasePostRequest(BaseModel):
    id: int


class GetPostRequest(BasePostRequest):
    pass


class DeletePostRequest(BasePostRequest):
    pass


class UpdateCreatePostRequest(BaseModel):
    title: str
    body: str
    user_id: int

    @validator('title')
    def title_check(cls, value):
        if value == '':
            raise ValueError('title not be empty')
        return value


class CreatePostRequest(UpdateCreatePostRequest):
    email: EmailStr


class UpdatePostRequest(UpdateCreatePostRequest):
    title: str | None
    body: str | None


# ===================================RESPONSE_SCHEMAS====================================

class PostCreateResponse(BaseModel):
    post_id: int


class Reaction(CustomBaseModel):
    like: int = 0
    dislike: int = 0


class PostResponse(CustomBaseModel):
    id: int
    title: str
    body: str
    user_id: int
    email: EmailStr
    created_date: datetime.datetime
    reaction: Reaction = None

    @validator("created_date", pre=True)
    def created_date_local_time(cls, value):
        local_tz = pytz.timezone('Europe/Moscow')
        return local_tz.normalize(value.astimezone(local_tz))
