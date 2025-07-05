from fastapi import APIRouter, FastAPI


def add_routes(routes: list[APIRouter], app: FastAPI, prefix: str = "/v1", redirect_slashes: bool = False) -> None:
    """Include the declared API routers into the global versioned application router."""
    app.router.redirect_slashes = redirect_slashes

    for route in routes:
        app.include_router(route, prefix=prefix)
