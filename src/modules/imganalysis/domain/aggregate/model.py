from dataclasses import dataclass
from pydantic import NonNegativeInt

from src.modules.imganalysis.domain.value_objects import Object, Region
from src.modules.imganalysis.usecase.new_heat_map.command import NewImageHeatMapCommand

from .id import ImageHeatMapId


@dataclass
class ImageHeatMap:
    id: ImageHeatMapId
    tracking_id: NonNegativeInt
    x_min_bb: float
    y_min_bb: float
    x_max_bb: float
    y_max_bb: float
    x_centroid_bb: float
    y_centroid_bb: float
    object_label: Object
    region_label: Region

    @staticmethod
    def new_heat_map(command: NewImageHeatMapCommand) -> 'ImageHeatMap':
        return ImageHeatMap(id=ImageHeatMapId.next_id(), **command.model_dump())
