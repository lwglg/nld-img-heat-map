from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field, UUID4

from webapp.core.fastapi.responses import create_data_model


class UserCreationSchema(BaseModel):
    email: EmailStr
    password: str
    hashed_password: str | None = None
    is_active: bool = False


class UserUpdateSchema(BaseModel):
    email: EmailStr | None = None
    password: str | None = None
    hashed_password: str | None = None
    is_active: bool | None = None


class UserDetailSchema(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    email: EmailStr
    is_active: bool


UserDetail = create_data_model(UserDetailSchema, custom_single_name="user")
UserDetails = create_data_model(
    UserDetailSchema, plural=True, custom_plural_name="users"
)
