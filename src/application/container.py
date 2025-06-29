from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from pymfdata.rdb.connection import AsyncSQLAlchemy

from settings import DB_SETTINGS


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
