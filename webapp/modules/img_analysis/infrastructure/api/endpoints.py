from fastapi import Depends, status
from fastapi_filter import FilterDepends
from dependency_injector.wiring import inject, Provide

from webapp.core.fastapi.responses import GenericResponse
from webapp.server.containers import Container
from webapp.modules.img_analysis.infrastructure.persistence.services import (
    ImageAnalysisService,
)
from webapp.modules.img_analysis.domain.schemas.img_analysis import (
    ImageAnalysisDetail,
    ImageAnalysisDetails,
    ImageAnalysisRequestBodySchema,
)


from . import img_analysis_router as router
from .filters import ImageAnalysisFilter


@router.get("/", response_model=GenericResponse[ImageAnalysisDetails])
@inject
async def list_analysis(
    analysis_filter: ImageAnalysisFilter = FilterDepends(ImageAnalysisFilter),
    img_analysis_service: ImageAnalysisService = Depends(
        Provide[Container.img_analysis_service]
    ),
):
    """Retrieve a list of analysis."""
    analysis = await img_analysis_service.list_analysis(analysis_filter)
    return {"status": status.HTTP_200_OK, "data": {"analysis": analysis}}


@router.get("/{analysis_id}", response_model=GenericResponse[ImageAnalysisDetail])
@inject
async def get_by_id(
    analysis_id: str,
    img_analysis_service: ImageAnalysisService = Depends(
        Provide[Container.img_analysis_service]
    ),
):
    """Retrieve analysis information, given a valid UUID4."""
    analysis = await img_analysis_service.analysis_by_id(analysis_id)
    return {"status": status.HTTP_200_OK, "data": {"analysis": analysis}}


@router.post("/", response_model=GenericResponse[ImageAnalysisDetails])
@inject
async def apply_image_analysis(
    payload: ImageAnalysisRequestBodySchema,
    img_analysis_service: ImageAnalysisService = Depends(
        Provide[Container.img_analysis_service]
    ),
):
    """Create a new analysis, given a valid payload."""
    analysis = await img_analysis_service.apply_image_analysis(payload)
    return {"status": status.HTTP_201_CREATED, "data": {"analysis": analysis}}


@router.delete("/{analysis_id}")
@inject
async def remove(
    analysis_id: str,
    img_analysis_service: ImageAnalysisService = Depends(
        Provide[Container.img_analysis_service]
    ),
):
    """Remove analysis information, given a valid UUID4."""
    await img_analysis_service.delete_by_id(analysis_id)

    return {"status": status.HTTP_204_NO_CONTENT}
