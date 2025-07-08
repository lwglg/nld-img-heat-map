from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import field_validator

from webapp.modules.img_analysis.domain.attributes import ImageAnalysisType
from webapp.modules.img_analysis.domain.models import ImageAnalysis


class ImageAnalysisFilter(Filter):
    object_label__ilike: str | None = None
    region_label__ilike: str | None = None
    image_path__ilike: str | None = None
    analysis_type__in: list[ImageAnalysisType] | None = None
    analysis_type: ImageAnalysisType | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):  # noqa: D106
        model = ImageAnalysis

    @field_validator("order_by")
    def restrict_sortable_fields(cls, value):
        if value is None:
            return None

        allowed_field_names = [
            "tracking_id",
            "x_min_bb",
            "y_min_bb",
            "x_max_bb",
            "y_max_bb",
            "x_centroid_bb",
            "y_centroid_bb",
        ]

        for field_name in value:
            field_name = field_name.replace("+", "").replace("-", "")

            if field_name not in allowed_field_names:
                raise ValueError(
                    f"Apenas os seguintes campos são ordenáveis: {', '.join(allowed_field_names)}"
                )

        return value
