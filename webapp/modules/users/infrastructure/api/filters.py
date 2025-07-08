from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import field_validator, EmailStr

from webapp.modules.users.domain.models import User


class UserFilter(Filter):
    email: EmailStr | None = None
    is_active: bool | None = None
    order_by: list[str] | None = None

    class Constants(Filter.Constants):  # noqa: D106
        model = User

    @field_validator("order_by")
    def restrict_sortable_fields(cls, value):
        if value is None:
            return None

        allowed_field_names = [
            "email",
        ]

        for field_name in value:
            field_name = field_name.replace("+", "").replace("-", "")

            if field_name not in allowed_field_names:
                raise ValueError(
                    f"Apenas os seguintes campos são ordenáveis: {', '.join(allowed_field_names)}"
                )

        return value
