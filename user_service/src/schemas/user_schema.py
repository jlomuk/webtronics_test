from pydantic import BaseModel, EmailStr
from pydantic.fields import Field


class User(BaseModel):
    id: int
    email: EmailStr
    password: str = Field(None, exclude=True)
