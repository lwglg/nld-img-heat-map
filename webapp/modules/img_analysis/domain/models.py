import inspect

from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    Enum,
    Integer,
    Numeric,
    String,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import UUID

from webapp.modules.shared.domain.models import UUID4PKMixin
from webapp.server.database import Base

from .attributes import ImageAnalysisType


class ImageAnalysis(UUID4PKMixin, Base):
    __tablename__ = "image_analysis"

    FP_PRECISION = 10  # number of total digits
    FP_DIGITS = 2  # digits after the decimal separator

    # Primary key (UUID4)
    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    # Unique tracking ID
    tracking_id = Column(Integer, CheckConstraint("tracking_id >= 0"), index=True)

    # Numeric data
    x_min_bb = Column(
        Numeric(precision=FP_PRECISION, scale=FP_DIGITS), nullable=False, default=0.0
    )
    y_min_bb = Column(
        Numeric(precision=FP_PRECISION, scale=FP_DIGITS), nullable=False, default=0.0
    )
    x_max_bb = Column(
        Numeric(precision=FP_PRECISION, scale=FP_DIGITS), nullable=False, default=0.0
    )
    y_max_bb = Column(
        Numeric(precision=FP_PRECISION, scale=FP_DIGITS), nullable=False, default=0.0
    )
    x_centroid_bb = Column(
        Numeric(precision=FP_PRECISION, scale=FP_DIGITS), nullable=False, default=0.0
    )
    y_centroid_bb = Column(
        Numeric(precision=FP_PRECISION, scale=FP_DIGITS), nullable=False, default=0.0
    )

    # Text data
    object_label = Column(String, nullable=False)
    region_label = Column(String, nullable=False)
    image_path = Column(String, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Categoric data
    analysis_type = Column(Enum(ImageAnalysisType), default=ImageAnalysisType.UNDEFINED)

    def __repr__(self) -> str:
        repr_str = f"<{ImageAnalysis.__class__.__name__}("

        raw_instance_attrs = inspect.getmembers(
            self, lambda a: not (inspect.isroutine(a))
        )
        instance_attrs = [
            a
            for a in raw_instance_attrs
            if not (a[0].startswith("__") and a[0].endswith("__"))
        ]

        for ix, (key, value) in enumerate(instance_attrs):
            if ix + 1 == len(instance_attrs):
                repr_str += f"{key}={value}"
                continue

            repr_str += f"{key}={value}, "

        return f"{repr_str})>"
