from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from webapp.core.fastapi.exceptions.handlers import init_error_handlers
from webapp.core.fastapi.routing import add_routers
from webapp.core.fastapi.openapi import apply_openapi_schema
from webapp.modules.users.infrastructure.api import (
    users_router,
    endpoints as users_endpoints,
)
from webapp.modules.img_analysis.infrastructure.api import (
    img_analysis_router,
    endpoints as img_analysis_endpoints,
)

from .containers import Container
from .events import build_lifespan_context_manager


def create_app() -> tuple[FastAPI, Container]:
    """Build the FastAPi application instance."""

    container = Container()
    container.wire(modules=[img_analysis_endpoints, users_endpoints])

    webapp_config = container.config.webapp
    swagger_ui_config = container.config.swagger_ui
    debug: bool = webapp_config.debug()
    root_path: str = webapp_config.api.root_path()

    fastapi_app = FastAPI(
        debug=debug,
        title=swagger_ui_config.page_title(),
        description=swagger_ui_config.description(),
        lifespan=build_lifespan_context_manager(container.db()),
        root_path=f"/{root_path}",
    )

    fastapi_app.mount("/static", StaticFiles(directory="static"), name="static")
    fastapi_app.container = container
    fastapi_app.openapi = apply_openapi_schema(fastapi_app, container.config)

    add_routers(
        fastapi_app,
        [img_analysis_router, users_router],
        api_version=webapp_config.api.version(),
    )
    init_error_handlers(fastapi_app, container.config.webapp.sysadmin.email())

    return fastapi_app, container


app, container = create_app()
