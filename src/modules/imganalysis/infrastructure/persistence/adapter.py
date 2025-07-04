from pymfdata.common.usecase import BaseUseCase
from pymfdata.rdb.transaction import async_transactional

from src.common.protocols.persistence_adapter import PersistenceAdapter
from src.modules.imganalysis.domain.aggregate.model import ImageHeatMap, ImageHeatMapId

from .uow import ImageHeatMapPersistenceUnitOfWork


class ImageHeatMapPersistenceAdapter(BaseUseCase[ImageHeatMapPersistenceUnitOfWork], PersistenceAdapter[ImageHeatMap, ImageHeatMapId]):
    def __init__(self, uow: ImageHeatMapPersistenceUnitOfWork) -> None:  # noqa: D107
        self._uow = uow

    @async_transactional(read_only=True)
    async def find_by_id(self, _id: ImageHeatMapId) -> ImageHeatMap:
        return await self.uow.repository.find_by_pk(_id)

    @async_transactional()
    async def insert(self, domain: ImageHeatMap) -> ImageHeatMap:
        self.uow.repository.create(domain)
        return domain

    @async_transactional()
    async def delete_by_id(self, _id: ImageHeatMap):
        entity = await self.uow.repository.find_by_pk(_id)
        if entity:
            await self.uow.repository.delete(entity)
