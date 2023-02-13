from typing import Any, Optional

from dotenv import find_dotenv
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    class Config:
        env_file = find_dotenv(usecwd=True)
        env_file_encoding = "utf-8"

    server_host: str
    server_port: int

    # Postgres DB
    database_host: str
    database_user: str
    database_password: str
    database_name: str
    database_uri: Optional[str] = None

    @validator("database_uri")
    def construct_database_connection_uri(cls, v: Optional[str], values: dict[str, Any]) -> str | PostgresDsn:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            host=values.get("database_host"),
            user=values.get("database_user"),
            password=values.get("database_password"),
            path=f"/{values.get('database_name') or ''}",
        )
