from sqlalchemy import Column, String, Boolean, text
from sqlalchemy.dialects.postgresql import UUID

from webapp.modules.shared.domain.models import UUID4PKMixin
from webapp.server.database import Base


class User(UUID4PKMixin, Base):
    __tablename__ = "users"

    id = Column(
        "id",
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=True)
    is_active = Column(Boolean, default=False, server_default="0")

    def __repr__(self):
        return f"<User(id='{self.id}', email='{self.email}', \
                hashed_password='{self.hashed_password}', \
                is_active='{self.is_active}')>"
