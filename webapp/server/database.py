from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from urllib.parse import quote_plus
from typing import Any

from dependency_injector.providers import Configuration
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from sqlalchemy.orm.decl_api import DeclarativeMeta
from sqlalchemy.pool import NullPool


Base: DeclarativeMeta = declarative_base()


class Database:
    def __init__(self, db_uri: str):
        """Connect to the database and create async session for queries."""
        self.db_uri = db_uri
        self.engine = create_async_engine(self.db_uri, poolclass=NullPool)
        self.session = scoped_session(
            sessionmaker(
                self.engine,
                autocommit=False,
                autoflush=False,
                class_=AsyncSession,
                expire_on_commit=False,
            )
        )

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[Any | AsyncSession, Any, None]:
        assert self._session_factory is not None

        session: AsyncSession = self.session_factory()
        try:
            yield session
        except Exception as exc:
            logger.error(f"Session rollback because of exception: %{exc}")
            session.rollback()
        finally:
            session.close()

    @staticmethod
    def build_db_connection_string(config: Configuration) -> str:
        """Build DB connection string from config YML file."""

        conn_str = "{engine}://{username}:{password}@{hostname}:{port}/{dbname}".format(  # noqa: UP032
            engine=config.db.engine(),
            username=config.db.username(),
            password=quote_plus(config.db.password()),
            hostname=config.db.hostname(),
            port=config.db.port(),
            dbname=config.db.dbname(),
        )

        return conn_str
