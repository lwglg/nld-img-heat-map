from pydantic import PositiveInt

from src.core.snowflake import seq


class ImageHeatMapId(PositiveInt):
    gt = 1

    @staticmethod
    def next_id() -> 'ImageHeatMapId':
        return ImageHeatMapId(seq.__next__())
