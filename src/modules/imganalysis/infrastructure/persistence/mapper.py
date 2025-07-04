from dataclasses import asdict
from pymfdata.rdb.mapper import mapper_registry

from common.protocols.model_mapper import ModelMapper
from src.modules.imganalysis.domain.aggregate.model import ImageHeatMap, ImageHeatMapId, TrackingId
from persistence.imganalysis.entity import ImageHeatMapEntity


class ImageHeatMapMapper(ModelMapper[ImageHeatMap, ImageHeatMapEntity]):
    @staticmethod
    def map_to_domain_entity(model: ImageHeatMapEntity) -> ImageHeatMap:
        return ImageHeatMap(
            id=ImageHeatMapId(model.id),
            tracking_id=TrackingId(model.tracking_id),
            x_min_bb=model.x_min_bb,
            y_min_bb=model.y_min_bb,
            x_max_bb=model.x_max_bb,
            y_max_bb=model.y_max_bb,
            x_centroid_bb=model.x_centroid_bb,
            y_centroid_bb=model.y_centroid_bb,
            region_label=model.region_label,
            object_label=model.object_label,
        )

    @staticmethod
    def map_to_persistence_entity(model: ImageHeatMap) -> ImageHeatMapEntity:
        return ImageHeatMapEntity(**asdict(model))


def start_mapper():  # noqa: D103
    t = ImageHeatMapEntity.__table__

    mapper_registry.map_imperatively(ImageHeatMap, t, )
