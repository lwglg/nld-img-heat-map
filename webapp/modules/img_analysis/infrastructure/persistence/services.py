from __future__ import annotations
from collections.abc import Awaitable, Callable

from loguru import logger

from webapp.modules.img_analysis.domain.schemas.img_analysis import (
    ImageAnalysisDetailSchema,
)
from webapp.modules.img_analysis.domain.schemas.img_heat_map import (
    ImageHeatMapCreationRequestSchema,
)
from webapp.modules.img_analysis.infrastructure.persistence.repositories import (
    ImageAnalysisRepository,
)


class ImageAnalysisService:
    def __init__(self, repository: ImageAnalysisRepository):
        """Associates DB repository to the service."""
        self.repository: ImageAnalysisRepository = repository

    async def list_analysis(self) -> Awaitable[list[ImageAnalysisDetailSchema] | None]:
        return await self.repository.get_all_analysis()

    async def analysis_by_id(
        self, analysis_id: str
    ) -> Awaitable[ImageAnalysisDetailSchema | None]:
        return await self.repository.get_by_id(analysis_id)

    async def delete_by_id(
        self, analysis_id: str
    ) -> Callable[[ImageAnalysisService, int], Awaitable[None]]:
        await self.repository.delete_by_id(analysis_id)

    async def create_img_heat_map(
        self, payload: ImageHeatMapCreationRequestSchema
    ) -> Awaitable[ImageAnalysisDetailSchema | None]:
        logger.warning(payload.model_dump())
