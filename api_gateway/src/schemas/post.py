import datetime

from pydantic import BaseModel, EmailStr

from schemas.auth import User
from schemas.custom_model import CustomBaseModel


class BasePostRequest(BaseModel):
    id: int


class GetPostRequest(BasePostRequest):
    pass


class DeletePostRequest(BasePostRequest):
    pass


class CreatePostRequest(BaseModel):
    title: str
    body: str
    user_id: int = None
    email: EmailStr = None

    def bind_user(self, user: User):
        self.user_id = user.id
        self.email = user.email


class UpdatePostRequest(BaseModel):
    title: str | None
    body: str | None
    user_id: int | None = None

    def bind_user(self, user: User):
        self.user_id = user.id


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
