from __future__ import annotations
from collections.abc import Callable

from fastapi import FastAPI
from contextlib import _AsyncGeneratorContextManager, asynccontextmanager
from sqlalchemy.orm import clear_mappers

from src.core.fastapi.error import init_error_handlers
from src.core.fastapi.event.middleware import EventHandlerMiddleware
from src.core.fastapi.responses import ORJSONResponse
from src.core.fastapi.routes import add_routes
from src.modules.imganalysis.usecase import router as img_analysis_router
from src.modules.imganalysis.usecase.new_heat_map import api as new_heat_map_api
from src.modules.imganalysis.infrastructure.persistence import mapper as img_analysis_persistence_mapper
from src.modules.imganalysis.infrastructure.query import mapper as img_analysis_query_mapper

from .container import Container, DeclarativeContainer, AsyncSQLAlchemy
from .settings import WEBSERVICE_SETTINGS


def build_di_container() -> tuple[DeclarativeContainer, AsyncSQLAlchemy]:
    """Build the dependency injection container and DB instances for the application."""

    # Insert Container (IoC)
    container = Container()
    container.wire(modules=[new_heat_map_api, ])

    db = container.db()

    return container, db


def build_context_manager(db: AsyncSQLAlchemy) -> Callable[[FastAPI,], _AsyncGeneratorContextManager[None, None]]:
    """Build the async function that handles tasks associated to startup and shutdown events."""

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        """Define the startup and shutdown logic associated to the webservice."""

        # Startup logic
        await db.connect(echo=True)
        await db.create_database()

        img_analysis_persistence_mapper.start_mapper()
        img_analysis_query_mapper.start_mapper()

        yield

        # Shutdown logic
        clear_mappers()

        await db.disconnect()

    return lifespan


class ApplicationFactory:
    """FastAPI application factory."""

    def __init__(self):
        """Declare an empty FastAPI application."""
        self.app: FastAPI | None = None

    def build_application(self, db_instance: AsyncSQLAlchemy, di_container: DeclarativeContainer) -> ApplicationFactory:
        self.app = FastAPI(
            default_response_class=ORJSONResponse,
            lifespan=build_context_manager(db_instance),
            debug=WEBSERVICE_SETTINGS.debug
        )

        self.app.container = di_container

        return self

    def add_routes(self) -> ApplicationFactory:
        if self.app is not None:
            add_routes([img_analysis_router], self.app)

        return self

    def apply_middlewares(self) -> ApplicationFactory:
        if self.app is not None:
            self.app.add_middleware(EventHandlerMiddleware)
            init_error_handlers(self.app, WEBSERVICE_SETTINGS.sysadmin_email)

        return self

    def get_instance(self) -> FastAPI | None:
        return self.app
