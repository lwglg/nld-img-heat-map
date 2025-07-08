from __future__ import annotations
from os import path
from collections.abc import Awaitable, Callable

from loguru import logger

from webapp.modules.img_analysis.domain.schemas.img_analysis import (
    ImageAnalysisDetailSchema,
    ImageAnalysisRequestBodySchema,
)
from webapp.modules.img_analysis.infrastructure.persistence.repositories import (
    ImageAnalysisRepository,
)
from webapp.modules.img_analysis.infrastructure.services import (
    file_retrieval as fr_service,
    img_processing as ip_service,
    tracking_data as td_service,
)
from webapp.modules.img_analysis.infrastructure.api.filters import ImageAnalysisFilter


class ImageAnalysisService:
    def __init__(self, repository: ImageAnalysisRepository):
        """Associates DB repository to the service."""
        self.repository: ImageAnalysisRepository = repository

    async def list_analysis(
        self, analysis_filter: ImageAnalysisFilter
    ) -> Awaitable[list[ImageAnalysisDetailSchema] | None]:
        return await self.repository.list_analysis(analysis_filter)

    async def analysis_by_id(
        self, analysis_id: str
    ) -> Awaitable[ImageAnalysisDetailSchema | None]:
        return await self.repository.get_by_id(analysis_id)

    async def delete_by_id(
        self, analysis_id: str
    ) -> Callable[[ImageAnalysisService, int], Awaitable[None]]:
        await self.repository.delete_by_id(analysis_id)

    async def _check_img_analysis_status(
        self, payload: ImageAnalysisRequestBodySchema
    ) -> Awaitable[list[ImageAnalysisDetailSchema] | None]:
        img_file_id = payload.image_file_google_drive_id
        object_label = payload.object_label
        analysis_type = payload.analysis_type
        output_img_path = ip_service.build_output_img_file(
            img_file_id, object_label, analysis_type.value
        )

        if not path.exists(output_img_path):
            return

        logger.warning(
            f"'{analysis_type.value}' already generated on file '{output_img_path}'. Returning persisted DB data instead..."
        )

        analysis_filter = ImageAnalysisFilter(
            analysis_type=analysis_type.value, image_path__ilike=output_img_path
        )

        return await self.repository.list_analysis(analysis_filter)

    async def apply_image_analysis(
        self, payload: ImageAnalysisRequestBodySchema
    ) -> Awaitable[list[ImageAnalysisDetailSchema] | None]:
        # Check if the requested analysis was already generated.
        analysis_records = await self._check_img_analysis_status(payload)

        if analysis_records:
            return analysis_records

        # Gather params from incoming payload
        json_file_id = payload.json_file_google_drive_id
        img_file_id = payload.image_file_google_drive_id
        object_label = payload.object_label
        analysis_type = payload.analysis_type

        # Perform the download of both JSON and PNG files
        fr_service.perform_download(
            [
                (json_file_id, "json"),
                (img_file_id, "png"),
            ],
        )

        # Loads the JSON file and extract the tracking messages for a specific object
        tracking_messages = td_service.obtain_tracking_messages(
            json_file_id, img_file_id, object_label, analysis_type
        )

        ip_service.perform_image_analysis(img_file_id, tracking_messages, analysis_type)

        if len(tracking_messages) > 0:
            # Save the generated bounding boxes into a single analysis batch for the same type
            analysis_records = await self.repository.add_analysis_bulk(
                tracking_messages
            )

            return analysis_records
