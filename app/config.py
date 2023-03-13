from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOSTNAME: str
    DB_USERNAME: str
    DB_NAME: str
    DB_PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
