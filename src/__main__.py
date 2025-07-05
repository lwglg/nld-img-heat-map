import sys

import uvicorn
from loguru import logger

from src.application.factory import build_di_container, ApplicationFactory
from src.application.settings import WEBSERVICE_SETTINGS


if __name__ == "__main__":
    try:
        di_container, db_instance = build_di_container()
        app = ApplicationFactory() \
            .build_application(db_instance, di_container) \
            .add_routes() \
            .apply_middlewares() \
            .get_instance()

        if app is None:
            raise Exception("FastAPI application instance not constructed properly. Not possible to run ASGI server.")

        uvicorn.run(
            app,
            host=WEBSERVICE_SETTINGS.host,
            port=WEBSERVICE_SETTINGS.port,
            log_level=WEBSERVICE_SETTINGS.log_level,
            lifespan="on"
        )
    except Exception as exc:
        logger.error(f"{exc.__class__.__name__}: {str(exc)}")
        sys.exit(-1)
