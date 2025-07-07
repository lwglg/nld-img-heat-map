from os import getenv

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration, Factory, Singleton

from webapp.server.database import Database
from webapp.modules.img_analysis.infrastructure.persistence.repositories import (
    ImageAnalysisRepository,
)
from webapp.modules.img_analysis.infrastructure.persistence.services import (
    ImageAnalysisService,
)
from webapp.modules.users.infrastructure.persistence.repositories import UserRepository
from webapp.modules.users.infrastructure.persistence.services import UserService


class Container(DeclarativeContainer):
    config = Configuration()
    config_yaml_path = getenv("CONFIG_YAML_PATH")

    if not config_yaml_path:
        raise Exception(
            "'CONFIG_YAML_PATH' variable not set. Application config cannot be retrieved."
        )

    config.from_yaml(config_yaml_path)

    db = Singleton(Database, db_uri=Database.build_db_connection_string(config))

    # Users domain
    users_repository = Factory(UserRepository, session_factory=db.provided.session)
    user_service = Factory(UserService, users_repository=users_repository)

    # Image analysis domain
    img_analysis_repository = Factory(
        ImageAnalysisRepository, session_factory=db.provided.session
    )
    img_analysis_service = Factory(
        ImageAnalysisService,
        img_analysis_repository=img_analysis_repository,
    )
