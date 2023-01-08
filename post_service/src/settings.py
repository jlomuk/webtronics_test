import logging
from logging.config import dictConfig

from pydantic import BaseSettings
from pydantic.networks import PostgresDsn

from logger import LogConfig

dictConfig(LogConfig().dict())
logger = logging.getLogger("post_service")

class Settings(BaseSettings):
    POSTGRES_URL: PostgresDsn = ''

    class Config():
        env_file = '.env'


settings = Settings()
