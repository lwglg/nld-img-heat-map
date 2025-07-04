from typing import TypedDict, Required
from pydantic import EmailStr
from os import getenv

from src.common.utils.parsing import to_boolean


__all__ = [
    "DB_SETTINGS",
    "WEBSERVICE_SETTINGS"
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
    port: Required[int]
    sysadmin_email: EmailStr
    log_level: Required[str]
    host: Required[str]


DB_SETTINGS = DatabaseSettings(
    db_engine=getenv("DB_ENGINE", "postgresql+asyncpg"),
    db_name=getenv("DB_NAME", "nld_img_analysis_db"),
    username=getenv("DB_USERNAME", "postgres"),
    password=getenv("DB_PASSWORD", "postgres"),
    hostname=getenv("DB_HOSTNAME", "127.0.0.1"),
    port=int(getenv("DB_PORT", 5432))
)


WEBSERVICE_SETTINGS = FastAPISettings(
    debug=to_boolean(getenv("APP_DEBUG", False)),
    port=getenv("APP_PORT", 5000),
    sysadmin_email=getenv("SYSADMIN_EMAIL", "lwglguilherme@gmail.com"),
    log_level=getenv("APP_LOG_LEVEL", "info"),
    host=getenv("APP_HOST", "127.0.0.1"),
)
