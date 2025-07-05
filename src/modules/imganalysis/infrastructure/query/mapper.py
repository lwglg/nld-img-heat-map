from pymfdata.rdb.mapper import mapper_registry

from src.persistence.imganalysis.entity import ImageHeatMapEntity

from .dto import ImageHeatMapDTO


def start_mapper():
    """Map a table entity into its respective DTO."""
    t = ImageHeatMapEntity.__table__

    mapper_registry.map_imperatively(ImageHeatMapDTO, t)
