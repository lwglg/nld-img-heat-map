from datetime import datetime
from uuid import uuid4

from pydantic import BaseModel, Field, UUID4

from webapp.core.fastapi.responses import create_data_model


class ImageAnalysisCreationSchema(BaseModel):
    tracking_id: int
    x_min_bb: float
    y_min_bb: float
    x_max_bb: float
    y_max_bb: float
    object_label: str
    region_label: str
    image_url: str


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
    image_url: str | None = None


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
    image_url: str
    created_at: datetime
    updated_at: datetime


ImageAnalysisDetail = create_data_model(
    ImageAnalysisDetailSchema, custom_single_name="analysis"
)
ImageAnalysisDetails = create_data_model(
    ImageAnalysisDetailSchema, plural=True, custom_plural_name="analysis"
)
