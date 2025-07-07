from uuid import uuid4

from pydantic import BaseModel, Field, UUID4

from webapp.core.fastapi.responses import create_data_model
from webapp.modules.img_analysis.domain.attributes import ImageAnalysisType


class ImageAnalysisCreationSchema(BaseModel):
    tracking_id: int
    x_min_bb: float
    y_min_bb: float
    x_max_bb: float
    y_max_bb: float
    object_label: str
    region_label: str
    image_path: str


class ImageAnalysisUpdateSchema(BaseModel):
    tracking_id: int | None = None
    x_min_bb: float | None = None
    y_min_bb: float | None = None
    x_max_bb: float | None = None
    y_max_bb: float | None = None
    x_centroid_bb: float | None = None
    y_centroid_bb: float | None = None
    object_label: str | None = None
    region_label: str | None = None
    image_path: str | None = None
    analysis_type: ImageAnalysisType = ImageAnalysisType.UNDEFINED.value


class ImageAnalysisDetailSchema(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    tracking_id: int
    x_min_bb: float
    y_min_bb: float
    x_max_bb: float
    y_max_bb: float
    x_centroid_bb: float
    y_centroid_bb: float
    object_label: str
    region_label: str
    image_path: str
    analysis_type: ImageAnalysisType


class ImageAnalysisRequestBodySchema(BaseModel):
    image_file_google_drive_id: str
    json_file_google_drive_id: str
    object_label: str
    analysis_type: ImageAnalysisType = ImageAnalysisType.UNDEFINED.value


ImageAnalysisDetail = create_data_model(
    ImageAnalysisDetailSchema, custom_single_name="analysis"
)
ImageAnalysisDetails = create_data_model(
    ImageAnalysisDetailSchema, plural=True, custom_plural_name="analysis"
)
