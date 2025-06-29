from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlalchemy.orm import clear_mappers

from container import Container
from core.fastapi.error import init_error_handler
from core.fastapi.event.middleware import EventHandlerMiddleware
from core.fastapi.responses import ORJSONResponse
from settings import FASTAPI_SETTINGS


# Insert Container (IoC)
container = Container()
db = container.db()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Define the startup and shutdown logic associated to the webservice."""

    # Startup logic
    await db.connect(echo=True)
    await db.create_database()

    yield

    # Shutdown logic
    clear_mappers()

    await db.disconnect()


app = FastAPI(default_response_class=ORJSONResponse, lifespan=lifespan)
app.container = container

app.add_middleware(EventHandlerMiddleware)
init_error_handler(app, FASTAPI_SETTINGS['sysadmin_email'])
