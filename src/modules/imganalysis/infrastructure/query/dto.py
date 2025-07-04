from dataclasses import dataclass


@dataclass
class ImageHeatMapDTO:
    id: int
    tracking_id: int
    x_min_bb: float
    y_min_bb: float
    x_max_bb: float
    y_max_bb: float
    x_centroid_bb: float
    y_centroid_bb: float
    object_label: str
    region_label: str
