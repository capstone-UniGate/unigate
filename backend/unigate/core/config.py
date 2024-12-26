from typing import Annotated

from pydantic import AnyUrl, BeforeValidator, PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from unigate.enums import Mode


def parse_cors(v: str | list[str]) -> list[str] | str:
    if isinstance(v, str) and not v.startswith("["):
        return [i.strip() for i in v.split(",")]
    return v


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )

    MODE: Mode = Mode.DEV
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    UNIGATE_DB: str = "unigate"
    AUTH_DB: str = "auth"
    SENDGRID_API_KEY: str
    JWT_SECRET: str
    JWT_EXPIRATION_SECONDS: int = 60 * 60 * 24  # 1 day
    JWT_ALGORITHM: str = "HS256"
    BACKEND_CORS_ORIGINS: Annotated[list[AnyUrl] | str, BeforeValidator(parse_cors)] = (
        "http://localhost,http://localhost:3000,https://localhost,https://localhost:3000"
    )
    MINIO_ENDPOINT: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str

    @computed_field  # type: ignore
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS]

    @computed_field  # type: ignore
    @property
    def UNIGATE_DB_URI(self) -> PostgresDsn:  # noqa: N802
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.UNIGATE_DB,
        )

    @computed_field  # type: ignore
    @property
    def AUTH_DB_URI(self) -> PostgresDsn:  # noqa: N802
        return PostgresDsn.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.AUTH_DB,
        )


settings = Settings()  # type: ignore
