from pymfdata.rdb.repository import AsyncRepository, AsyncSession

from src.modules.imganalysis.domain.aggregate.model import ImageHeatMap


class ImageHeatMapRepository(AsyncRepository[ImageHeatMap, int]):
    def __init__(self, session: AsyncSession) -> None:  # noqa: D107
        self._session = session
