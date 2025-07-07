import uuid

from sqlalchemy.orm import declarative_mixin
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import UUID


@declarative_mixin
class UUID4PKMixin:
    def __init__(self, **kwargs):
        """Generate the default UUID if the latter is not informed in the kwargs."""

        if "id" not in kwargs:
            kwargs["id"] = uuid.uuid4()
        super().__init__(**kwargs)

    id: uuid.UUID = Column(
        UUID(as_uuid=True), primary_key=True, server_default="gen_random_uuid()"
    )
