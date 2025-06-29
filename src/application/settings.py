from typing import TypedDict, Required
from pydantic import EmailStr
from os import getenv

from common.utils.parsing import to_boolean


__all__ = [
    "DB_SETTINGS",
    "FASTAPI_SETTINGS"
]


class DatabaseSettings(TypedDict):
    db_engine: Required[str]
    db_name: Required[str]
    username: Required[str]
    password: Required[str]
    hostname: Required[str]
    port: Required[int]


class FastAPISettings(TypedDict):
    debug: bool
    port: Required[dict]
    sysadmin_email: EmailStr


class AppSettings(TypedDict):
    database: DatabaseSettings
    fastapi: FastAPISettings


DB_SETTINGS = DatabaseSettings(
    db_engine=getenv("DB_ENGINE", "postgresql+asyncpg"),
    db_name=getenv("DB_NAME", "nld_img_analysis_db"),
    username=getenv("DB_USERNAME", "postgres"),
    password=getenv("DB_PASSWORD", "postgres"),
    hostname=getenv("DB_HOSTNAME", "127.0.0.1"),
    port=getenv("DB_PORT", 5432)
)


FASTAPI_SETTINGS = FastAPISettings(
    debug=to_boolean(getenv("APP_DEBUG", False)),
    port=getenv("APP_PORT", 5000),
    sysadmin_email=getenv("SYSADMIN_EMAIL", "lwglguilherme@gmail.com"),
)
