from fastapi import Depends, status
from fastapi_filter import FilterDepends
from dependency_injector.wiring import inject, Provide

from webapp.core.fastapi.responses import GenericResponse
from webapp.server.containers import Container
from webapp.modules.users.infrastructure.persistence.services import UserService
from webapp.modules.users.domain.schemas import (
    UserCreationSchema,
    UserUpdateSchema,
    UserDetail,
    UserDetails,
)

from . import users_router as router
from .filters import UserFilter


@router.get("", response_model=GenericResponse[UserDetails])
@inject
async def list_users(
    user_filter: UserFilter = FilterDepends(UserFilter),
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    """Retrieve a list of users."""
    users = await user_service.list_users(user_filter)
    return {"status": status.HTTP_200_OK, "data": {"users": users}}


@router.get("/{user_id}", response_model=GenericResponse[UserDetail])
@inject
async def get_by_id(
    user_id: str, user_service: UserService = Depends(Provide[Container.user_service])
):
    """Retrieve user information, given a valid UUID4."""
    user = await user_service.user_by_id(user_id)
    return {"status": status.HTTP_200_OK, "data": {"user": user}}


@router.post("", response_model=GenericResponse[UserDetail])
@inject
async def create_user(
    payload: UserCreationSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    """Create a new user, given a valid payload."""
    user = await user_service.create_user(payload)
    return {"status": status.HTTP_201_CREATED, "data": {"user": user}}


@router.patch("/{user_id}", response_model=GenericResponse[UserDetail])
@inject
async def update_user(
    user_id: str,
    payload: UserUpdateSchema,
    user_service: UserService = Depends(Provide[Container.user_service]),
):
    """Create a new user, given a valid payload."""
    user = await user_service.update_user(user_id, payload)
    return {"status": status.HTTP_200_OK, "data": {"user": user}}


@router.delete("/{user_id}")
@inject
async def remove(
    user_id: str, user_service: UserService = Depends(Provide[Container.user_service])
):
    """Remove user information, given a valid UUID4."""
    await user_service.delete_by_id(user_id)

    return {"status": status.HTTP_204_NO_CONTENT}
