from webapp.common.utils.enums import BaseEnum


class ImageAnalysisType(BaseEnum):
    HEAT_MAP = "heat-map"
    BOUNDING_BOX = "bounding-box"
    UNDEFINED = "undefined"
