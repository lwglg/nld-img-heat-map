from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Factory, Singleton
from pymfdata.rdb.connection import AsyncSQLAlchemy

from .settings import DB_SETTINGS

from src.modules.imganalysis.infrastructure.persistence.adapter import ImageHeatMapPersistenceAdapter
from src.modules.imganalysis.infrastructure.persistence.uow import ImageHeatMapPersistenceUnitOfWork
from src.modules.imganalysis.usecase.new_heat_map.impl import NewImageHeatMapUseCase


class Container(DeclarativeContainer):
    db_conn_str = '{engine}://{username}:{password}@{host}:{port}/{db_name}'.format(
        engine=DB_SETTINGS["db_engine"],
        username=DB_SETTINGS['username'],
        password=DB_SETTINGS['password'],
        host=DB_SETTINGS['hostname'],
        port=DB_SETTINGS['port'],
        db_name=DB_SETTINGS['db_name'],
    )

    db = Singleton(AsyncSQLAlchemy, db_uri=db_conn_str)

    # Units Of Work
    img_heat_map_persistence_unit_of_work = Factory(ImageHeatMapPersistenceUnitOfWork, engine=db.provided.engine)

    # Adapters (If you use traditional mapper)
    img_heat_map_persistence_adapter = Factory(ImageHeatMapPersistenceAdapter, uow=img_heat_map_persistence_unit_of_work)

    # Use cases
    new_img_heat_map_use_case = Factory(NewImageHeatMapUseCase, uow=img_heat_map_persistence_unit_of_work)
