from pydantic import BaseModel, Field, HttpUrl, FileUrl


class ElasticSearchRequestPayload(BaseModel):
    deepstream_msg: list[str] = Field(alias="deepstream-msg")


class ImageHeatMapCreationRequestSchema(BaseModel):
    image_url: HttpUrl | FileUrl
    object_label: str
    elasticsearch_payload: ElasticSearchRequestPayload
