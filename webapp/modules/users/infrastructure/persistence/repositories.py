from collections.abc import Awaitable

from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from webapp.common.utils.security import Password
from webapp.core.fastapi.exceptions.classes import NotFoundException
from webapp.modules.users.domain.models import User
from webapp.modules.users.domain.schemas import UserCreationSchema, UserUpdateSchema
from webapp.modules.users.infrastructure.api.filters import UserFilter


class UserRepository:
    def __init__(self, session_factory: AsyncSession):
        """Associates DB async session."""
        self._session = session_factory

    async def _get_user_by_uuid(
        self, session: AsyncSession, user_id: str
    ) -> Awaitable[User | None]:
        result = await session.execute(select(User).where(User.id == user_id))
        existing_user = result.scalar()

        if not existing_user:
            raise NotFoundException(f'User with ID "{user_id}" not found')

        return existing_user

    async def get_by_id(self, user_id: str):
        async with self._session() as s:
            existing_user = await self._get_user_by_uuid(s, user_id)

            return existing_user

    async def list_users(self, user_filter: UserFilter):
        async with self._session() as s:
            query = select(User)
            query = user_filter.filter(query)
            result = await s.execute(query)
            users = result.scalars().all()

            return users

    async def add_user(self, payload: UserCreationSchema):
        async with self._session() as s:
            payload_dump = payload.model_dump()

            plain_password = payload_dump.get("password")
            payload_dump.update(
                {"hashed_password": Password.hash_password(plain_password)}
            )

            del payload_dump["password"]

            created_user = User(**payload_dump)
            s.add(created_user)
            await s.commit()

            return created_user

    async def update_user(self, user_id: str, payload: UserUpdateSchema):
        async with self._session() as s:
            await self._get_user_by_uuid(s, user_id)

            values_to_update = {}
            payload_dump = payload.model_dump()

            for key, value in payload_dump.items():
                if value is None:
                    continue

                if key == "password":
                    values_to_update.update(
                        {"hashed_password": Password.hash_password(value)}
                    )
                    del payload_dump[key]
                    continue

                values_to_update.update({key: value})

            stmt = (
                update(User)
                .values(**values_to_update)
                .where(User.id == user_id)
                .returning(User)
            )
            result = await s.execute(stmt)
            data = result.one()
            updated_user = User(**data)

            await s.commit()

            return updated_user

    async def delete_by_id(self, user_id: str):
        async with self._session() as s:
            await self._get_user_by_uuid(s, user_id)

            stmt = delete(User).where(User.id == user_id)

            await s.execute(stmt)
            await s.commit()
