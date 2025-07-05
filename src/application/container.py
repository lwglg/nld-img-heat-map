from loguru import logger
from urllib.parse import quote_plus
from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Resource, Singleton
from pymfdata.rdb.connection import AsyncSQLAlchemy

from .settings import DB_SETTINGS

from src.modules.imganalysis.infrastructure.persistence.adapter import ImageHeatMapPersistenceAdapter
from src.modules.imganalysis.infrastructure.persistence.uow import ImageHeatMapPersistenceUnitOfWork
from src.modules.imganalysis.usecase.new_heat_map.impl import NewImageHeatMapUseCase


class Container(DeclarativeContainer):
    logging = Resource(logger)

    # Database client for PostgreSQL
    db_conn_str = f'{DB_SETTINGS.db_engine}://{DB_SETTINGS.username}:{quote_plus(DB_SETTINGS.password)}@{DB_SETTINGS.hostname}:{DB_SETTINGS.port}/{DB_SETTINGS.db_name}'
    db = Singleton(AsyncSQLAlchemy, db_uri=db_conn_str)

    # Units Of Work
    img_heat_map_persistence_unit_of_work = Factory(ImageHeatMapPersistenceUnitOfWork, engine=db.provided.engine)

    # Adapters (If you use traditional mapper)
    img_heat_map_persistence_adapter = Factory(ImageHeatMapPersistenceAdapter, uow=img_heat_map_persistence_unit_of_work)

    # Use cases
    new_img_heat_map_use_case = Factory(NewImageHeatMapUseCase, uow=img_heat_map_persistence_unit_of_work)
