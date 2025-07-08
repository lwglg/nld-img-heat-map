from __future__ import annotations
from collections.abc import Awaitable

from webapp.modules.users.domain.schemas import UserCreationSchema, UserDetailSchema
from webapp.modules.users.infrastructure.api.filters import UserFilter
from webapp.modules.users.infrastructure.persistence.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        """Associates DB repository to the service."""
        self.repository: UserRepository = repository

    async def list_users(
        self, user_filter: UserFilter
    ) -> Awaitable[list[UserDetailSchema] | None]:
        return await self.repository.list_users(user_filter)

    async def user_by_id(self, user_id: str) -> Awaitable[UserDetailSchema | None]:
        return await self.repository.get_by_id(user_id)

    async def delete_by_id(self, user_id: str) -> Awaitable[None]:
        await self.repository.delete_by_id(user_id)

    async def create_user(
        self, payload: UserCreationSchema
    ) -> Awaitable[UserDetailSchema]:
        return await self.repository.add_user(payload)

    async def update_user(
        self, user_id: str, payload: UserCreationSchema
    ) -> Awaitable[UserDetailSchema]:
        return await self.repository.update_user(user_id, payload)
