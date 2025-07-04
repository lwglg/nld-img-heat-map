from pymfdata.common.usecase import BaseUseCase
from pymfdata.rdb.transaction import async_transactional

from src.modules.imganalysis.domain.aggregate.model import ImageHeatMap
from src.modules.imganalysis.usecase.new_heat_map.command import NewImageHeatMapCommand
from src.modules.imganalysis.infrastructure.persistence.uow import ImageHeatMapPersistenceUnitOfWork


class NewImageHeatMapUseCase(BaseUseCase[ImageHeatMapPersistenceUnitOfWork]):
    def __init__(self, uow: ImageHeatMapPersistenceUnitOfWork) -> None:
        """Associates Unit-of-Work to the use case."""
        self._uow = uow

    @async_transactional()
    async def invoke(self, command: NewImageHeatMapCommand) -> ImageHeatMap:
        img_analysis = ImageHeatMap.new_heat_map(command)
        self.uow.repository.create(img_analysis)

        return img_analysis
