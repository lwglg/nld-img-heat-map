from collections.abc import Callable
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager

from fastapi import FastAPI

from .database import Database, Base


def build_lifespan_context_manager(
    db: Database,
) -> Callable[
    [
        FastAPI,
    ],
    _AsyncGeneratorContextManager[None, None],
]:
    """Build the corroutine that handles tasks associated to startup and shutdown events."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Define the startup and shutdown logic associated to the webservice."""

        # Startup logic
        async with db.engine.begin() as db_conn:
            await db_conn.run_sync(Base.metadata.create_all)

        yield

        # Shutdown logic here

    return lifespan
