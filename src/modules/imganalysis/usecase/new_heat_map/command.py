from pydantic import ConfigDict, BaseModel, Field

from src.modules.imganalysis.domain.aggregate.id import TrackingId
from src.modules.imganalysis.domain.value_objects import Object, Region


class NewImageHeatMapCommand(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    tracking_id: TrackingId = Field(title="TRACKING-ID", description="Non-negative integer, uniquely identifying the tracking of an object")
    x_min_bb: float = Field(title="X-MIN-BB", description="Bounding box lower left X coordinate")
    y_min_bb: float = Field(title="X-MAX-BB", description="Bounding box lower left Y coordinate")
    x_max_bb: float = Field(title="Y-MIN-BB", description="Bounding box upper right X coordinate")
    y_max_bb: float = Field(title="Y-MAX-BB", description="Bounding box upper right Y coordinate")
    x_centroid_bb: float = Field(title="Y-CENTROID-BB", description="Bounding box centroid X coordinate")
    y_centroid_bb: float = Field(title="Y-CENTROID-BB", description="Bounding box centroid Y coordinate")
    object_label: Object = Field(title="OBJECT", description="Label of the object within the image")
    region_label: Region = Field(title="REGION", description="Region that the object is occupying in the image")
