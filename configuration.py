import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    POSTGRES_USER: str = 'hello'
    POSTGRES_PASSWORD: str = 'hello'
    POSTGRES_SERVER: str = 'localhost'
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str = "gh"
    DATABASE_URL: str = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}"

    GIT_DOMAIN: str
    GIT_TOKEN: str


settings = Settings(_env_file='.env')
