from pymfdata.rdb.mapper import Base
from sqlalchemy import Column, BigInteger, Integer, String, Float


class ImageHeatMapEntity(Base):
    __tablename__ = 'image_heat_map'
    FP_PRECISION = 4

    id: int | Column = Column(BigInteger, primary_key=True)
    tracking_id: int | Column = Column(Integer, nullable=False, unique=True)

    x_min_bb: float | Column = Column(Float(FP_PRECISION), nullable=False, default=0.0)
    y_min_bb: float | Column = Column(Float(FP_PRECISION), nullable=False, default=0.0)
    x_max_bb: float | Column = Column(Float(FP_PRECISION), nullable=False, default=0.0)
    y_max_bb: float | Column = Column(Float(FP_PRECISION), nullable=False, default=0.0)
    x_centroid_bb: float | Column = Column(Float(FP_PRECISION), nullable=False, default=0.0)
    y_centroid_bb: float | Column = Column(Float(FP_PRECISION), nullable=False, default=0.0)

    region_label: str | Column = Column(String(20), nullable=False)
    object_label: str | Column = Column(String(50), nullable=False)
