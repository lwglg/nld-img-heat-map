from __future__ import annotations
from collections.abc import Awaitable, Callable

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


class ImageAnalysisService:
    def __init__(self, img_analysis_repository: ImageAnalysisRepository):
        """Associates DB repository to the service."""
        self.repository: ImageAnalysisRepository = img_analysis_repository

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

    async def create_img_bounding_boxes(
        self, payload: ImageAnalysisRequestBodySchema
    ) -> Awaitable[list[ImageAnalysisDetailSchema] | None]:
        # Gather params from incoming payload
        json_file_id = payload.json_file_google_drive_id
        img_file_id = payload.image_file_google_drive_id
        object_label = payload.object_label
        analysis_type=payload.analysis_type

        # Perform the download of both JSON and PNG files
        fr_service.perform_download(
            [
                (json_file_id, "json"),
                (img_file_id, "png"),
            ],
        )

        # Loads the JSON file and extract the tracking messages for a specific object
        json_data = td_service.load_json_from_file(json_file_id)
        tracking_data = td_service.extract_tracking_data(json_data)
        tracking_messages = td_service.filter_tracking_data_by_object(
            tracking_data, object_label, analysis_type, img_file_id
        )

        if len(tracking_messages) > 0:
            # Loads the PNG image and generates the bounding boxes for a specific object
            img_data = ip_service.load_image_data(img_file_id)
            ip_service.draw_bounding_boxes(img_file_id, img_data, tracking_messages)

            # Save the generated bounding boxes into a single analysis batch for the same time
            analysis_records = await self.repository.add_analysis_bulk(tracking_messages)

            return analysis_records
