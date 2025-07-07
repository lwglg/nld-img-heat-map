from typing import Any
from collections.abc import Callable

from dependency_injector.providers import Configuration
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def apply_openapi_schema(
    app: FastAPI, config: Configuration
) -> Callable[..., dict[str, Any]]:
    """Generate the callable that applies the custom parameters for the OpenAPI UI."""

    def custom_openapi():
        """Override the default schema building for both /docs and /redoc."""
        if app.openapi_schema:
            return app.openapi_schema

        title: str = config.swagger_ui.page_title()
        version: str = config.swagger_ui.api_version()
        summary: str = config.swagger_ui.summary()
        description: str = config.swagger_ui.description()
        hostname: str = config.webapp.hostname()
        port: int = config.webapp.port()

        base_url = f"http://{'localhost' if hostname == '0.0.0.0' else hostname}:{port}{app.root_path}"

        openapi_schema = get_openapi(
            title=title,
            version=version,
            summary=summary,
            description=description,
            routes=app.routes,
            servers=[
                {
                    "description": "Development",
                    "url": base_url,
                }
            ],
        )

        redoc_logo = config.swagger_ui.redoc_logo

        openapi_schema["info"]["x-logo"] = {
            "url": f"{base_url}/{redoc_logo.path()}",
            "altText": redoc_logo.alt_text(),
            "backgroundColor": redoc_logo.background_color(),
            "href": redoc_logo.href(),
            "width": redoc_logo.width(),
            "height": redoc_logo.height(),
        }

        return openapi_schema

    return custom_openapi
