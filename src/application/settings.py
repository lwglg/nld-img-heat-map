from os import getenv

from pydantic import BaseModel, EmailStr

from src.common.utils.parsing import to_boolean


__all__ = [
    "DB_SETTINGS",
    "WEBSERVICE_SETTINGS"
]


class DatabaseSettings(BaseModel):
    db_engine: str
    db_name: str
    username: str
    password: str
    hostname: str
    port: int


class FastAPISettings(BaseModel):
    debug: bool
    port: int
    sysadmin_email: EmailStr
    log_level: str
    host: str


DB_SETTINGS = DatabaseSettings(
    db_engine=getenv("DB_ENGINE", "postgresql+asyncpg"),
    db_name=getenv("DB_NAME", "nld_img_analysis_db"),
    username=getenv("DB_USERNAME", "postgres"),
    password=getenv("DB_PASSWORD", "postgres"),
    hostname=getenv("DB_HOSTNAME", "127.0.0.1"),
    port=getenv("DB_PORT", 5432)
)


WEBSERVICE_SETTINGS = FastAPISettings(
    debug=to_boolean(getenv("APP_DEBUG", False)),
    port=getenv("APP_PORT", 5000),
    sysadmin_email=getenv("SYSADMIN_EMAIL", "lwglguilherme@gmail.com"),
    log_level=getenv("APP_LOG_LEVEL", "info"),
    host=getenv("APP_HOST", "127.0.0.1"),
)
