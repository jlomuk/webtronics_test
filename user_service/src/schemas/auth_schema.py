from pydantic import BaseModel, EmailStr
from pydantic.class_validators import validator, root_validator
from pydantic.fields import Field
from services.auth_service import AuthService


class AuthBase(BaseModel):
    email: EmailStr
    password: str

    @root_validator
    def validators_password(cls, values):
        values = cls.hash_password(values)
        return values

    @staticmethod
    def hash_password(values):
        password, password_repeat = values.get('password'), values.get('password_repeat')
        if password:
            values['password'] = AuthService.hash_password(password)
        if password_repeat:
            values['password_repeat'] = AuthService.hash_password(password_repeat)
        return values


class LoginRequest(AuthBase):
    pass


class RegistrationRequest(AuthBase):
    password_repeat: str = Field(..., exclude=True)

    @validator('password_repeat')
    def passwords_check(cls, v, values):
        if len(v) < 8:
            raise ValueError('Пароль меньше 8 символов')
        if v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v
