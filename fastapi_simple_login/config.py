from typing import Any, Dict, Optional
from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "test"
    DB_PWD: str = "test"
    DB_NAME: str = "test"
    DB_URI: Optional[PostgresDsn] = None

    ROOT_EMAIL = "root@example.com"
    ROOT_PASSWORD = "password"

    ORIGIN = "example.com"
    CLIENT_SECRET = "secret"
    TOKEN_VALIDITY_DAYS = 14

    @validator("DB_URI", pre=True)
    def assemble_db_connection(
        cls, v: Optional[str], values: Dict[str, Any] # noqa
    ) -> Any:
        if isinstance(v, str):
            return v

        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("DB_USER"),
            password=values.get("DB_PWD"),
            host=values.get("DB_HOST"),
            port=str(values.get("DB_PORT")),
            path=f"/{values.get('DB_NAME') or ''}",
        )


settings = Settings()
