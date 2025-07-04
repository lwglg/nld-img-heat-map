from pydantic import PositiveInt, NonNegativeInt

from src.core.snowflake import seq


class ImageHeatMapId(PositiveInt):
    gt = 1

    @staticmethod
    def next_id() -> 'ImageHeatMapId':
        return ImageHeatMapId(seq.__next__())


class TrackingId(NonNegativeInt):
    gt = 0
