from abc import abstractmethod
from typing import Protocol

from src.modules.imganalysis.infrastructure.query.dto import ImageHeatMapDTO


class ImageHeatMapQueryRepository(Protocol):
    @abstractmethod
    async def fetch_by_title(self, title: str) -> ImageHeatMapDTO:
        ...

    @abstractmethod
    async def fetch_by_id(self, _id: int) -> ImageHeatMapDTO:
        ...
