from collections.abc import Awaitable

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.core.fastapi.exceptions.classes import NotFoundException
from webapp.modules.img_analysis.domain.models import ImageAnalysis
from webapp.modules.img_analysis.domain.schemas.img_analysis import (
    ImageAnalysisCreationSchema,
)


class ImageAnalysisRepository:
    def __init__(self, session_factory: AsyncSession):
        """Associates DB async session."""
        self._session = session_factory

    async def _get_analysis_by_uuid(
        self, session: AsyncSession, analysis_id: str
    ) -> Awaitable[ImageAnalysis | None]:
        result = await session.execute(
            select(ImageAnalysis).where(ImageAnalysis.id == analysis_id)
        )
        existing_analysis = result.scalar()

        if not existing_analysis:
            raise NotFoundException(f'Image analysis with ID "{analysis_id}" not found')

        return existing_analysis

    async def get_by_id(self, analysis_id: str):
        async with self._session() as s:
            existing_analysis = await self._get_analysis_by_uuid(s, analysis_id)

            return existing_analysis

    async def delete_by_id(self, analysis_id: str):
        async with self._session() as s:
            await self._get_analysis_by_uuid(s, analysis_id)

            stmt = delete(ImageAnalysis).where(ImageAnalysis.id == analysis_id)

            await s.execute(stmt)
            await s.commit()

    async def get_all_analysis(self):
        async with self._session() as s:
            result = await s.execute(select(ImageAnalysis))
            analysis = result.scalars().all()

            return analysis

    async def add_analysis(self, payload: ImageAnalysisCreationSchema):
        async with self._session() as s:
            payload_dump = payload.model_dump()
            created_analysis = ImageAnalysis(**payload_dump)
            s.add(created_analysis)

            await s.commit()

            return created_analysis

    async def add_analysis_bulk(self, payload: list[ImageAnalysisCreationSchema]):
        async with self._session() as s:
            batch_to_insert = [item.model_dump() for item in payload]

            await s.run_sync(lambda ses: ses.bulk_insert_mappings(ImageAnalysis, batch_to_insert))
            await s.commit()

            return [ImageAnalysis(**item) for item in batch_to_insert]
