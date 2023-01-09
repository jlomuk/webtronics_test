from pydantic import BaseModel


class SuccessHunter(BaseModel):
    status: str
    email: str


class ErrorHunter(BaseModel):
    id: str
    code: int


class ResponseHunter(BaseModel):
    data: SuccessHunter = None
    errors: list[ErrorHunter] = None
