from pydantic import BaseSettings, EmailStr, SecretStr, validator, AnyHttpUrl


class Settings(BaseSettings):
    USER_BACKEND_SERVICE: str = ''
    TASK_BACKEND_SERVICE: str = ''

    class Config:
        env_file = '.env'


settings = Settings()
