from pymfdata.rdb.connection import AsyncEngine
from pymfdata.rdb.usecase import AsyncSQLAlchemyUnitOfWork

from src.modules.imganalysis.infrastructure.query.repository.impl import ImageHeatMapAlchemyRepository, ImageHeatMapQueryRepository


class ImageHeatMapQueryUnitOfWork(AsyncSQLAlchemyUnitOfWork):
    def __init__(self, engine: AsyncEngine) -> None:  # noqa: D107
        super().__init__(engine)

    async def __aenter__(self):
        await super().__aenter__()

        self.repository: ImageHeatMapQueryRepository = ImageHeatMapAlchemyRepository(self.session)
