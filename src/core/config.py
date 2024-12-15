import logging
from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import Field, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL
from typing_extensions import Self

BASE_DIR = Path(__file__).parent.parent
LOG_FORMAT = ""
LOG_FILEPATH = ""


class CommonSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="allow",
    )


class DatabaseSettings(CommonSettings):
    db_host: str = Field(default="localhost", alias="DB_HOST")
    db_user: str = Field(default="postgres", alias="DB_USER")
    db_password: str = Field(default="postgres", alias="DB_PASSWORD")
    db_port: int = Field(default=5432, alias="DB_PORT")
    db_name: str = Field(default="books_db", alias="DB_NAME")
    async_db_url: Optional[URL] = Field(default=None)
    sync_db_url: Optional[URL] = Field(default=None)
    raw_dns_string: Optional[str] = Field(default=None)

    def create_raw_dns(self) -> str:
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"

    @staticmethod
    def _create_db_dsn(
        username: str,
        password: str,
        host: str,
        port: int,
        database: str,
        async_status: bool,
    ) -> URL:
        driver_name = "postgresql"
        if async_status:
            driver_name += "+asyncpg"
        return URL.create(
            drivername=driver_name,
            username=username,
            password=password,
            host=host,
            port=port,
            database=database,
        )

    @model_validator(mode="after")
    def create_async_db_dsn(self) -> Self:
        self.async_db_url = self._create_db_dsn(
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            async_status=True,
        )
        return self

    @model_validator(mode="after")
    def create_sync_db_dsn(self) -> Self:
        self.sync_db_url = self._create_db_dsn(
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            async_status=False,
        )
        return self


class LoggingSettings(BaseSettings):
    log_filepath: Optional[Path] = Field(default=LOG_FILEPATH)
    format: Optional[str] = Field(default=LOG_FORMAT)
    log_mode: dict[str, int] = Field(
        default={
            "DEBUG": logging.DEBUG,
            "INFO": logging.DEBUG,
            "WARNING": logging.WARNING,
            "ERROR": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
        }
    )


class DatabaseHelper(BaseSettings):
    echo: bool = Field(default=False)
    echo_pool: bool = Field(default=False)
    pool_size: int = Field(default=0)
    max_overflow: int = Field(default=5)


class ServerSettings(BaseSettings):
    host: str = Field(default="localhost", alias="APP_HOST")
    port: int = Field(default=8080, alias="APP_PORT")


class Settings(CommonSettings):
    server: ServerSettings = ServerSettings()
    db: DatabaseSettings = DatabaseSettings()
    helper: DatabaseHelper = DatabaseHelper()
    logging: LoggingSettings = LoggingSettings()


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
