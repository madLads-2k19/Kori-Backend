from typing import Any

from dotenv import find_dotenv
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    class Config:
        env_file = find_dotenv(usecwd=True)
        env_file_encoding = "utf-8"

    SERVER_HOST: str
    SERVER_PORT: int
    APP_TITLE: str = "Kori Backend"

    # Postgres DB
    DATABASE_HOST: str
    DATABASE_USER: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_URI: str | None = None

    @validator("DATABASE_URI")
    def construct_database_connection_uri(cls, v: str | None, values: dict[str, Any]) -> str | PostgresDsn:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("DATABASE_HOST"),
            user=values.get("DATABASE_USER"),
            password=values.get("DATABASE_PASSWORD"),
            path=f"/{values.get('DATABASE_NAME') or ''}",
        )
