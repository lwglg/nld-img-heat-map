from pymfdata.rdb.repository import AsyncSession, BaseAsyncRepository
from sqlalchemy import select

from src.modules.imganalysis.infrastructure.query.dto import ImageHeatMapDTO
from src.modules.imganalysis.infrastructure.query.repository.protocol import ImageHeatMapQueryRepository


class ImageHeatMapAlchemyRepository(BaseAsyncRepository, ImageHeatMapQueryRepository):
    def __init__(self, session: AsyncSession) -> None:  # noqa: D107
        self._session = session

    async def fetch_by_region(self, region_label: str) -> ImageHeatMapDTO:
        stmt = select(ImageHeatMapDTO).where(ImageHeatMapDTO.region_label == region_label)

        result = await self.session.execute(stmt)
        return result.unique().scalars().fetchall()

    async def fetch_by_id(self, _id: int) -> ImageHeatMapDTO:
        stmt = select(ImageHeatMapDTO).where(ImageHeatMapDTO.id == _id)

        result = await self.session.execute(stmt)
        return result.unique().scalars().one_or_none()
