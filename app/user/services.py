from typing import Optional
from uuid import UUID

from fastapi import HTTPException

from app.auth.hasher import hash_password
from app.auth.schemas import Credentials
from app.user.entities import User
from app.user.models import User as ModelUser
from general_enum.permissions import Permissions
from ports.uow import AbstractUow


def get_by_id(uow: AbstractUow, user_id: UUID) -> Optional[User]:
    with uow:
        return uow.user.get(user_id)


def get_user_by_email(uow: AbstractUow, email: str) -> Optional[User]:
    with uow:
        return uow.user.get_by_email(email)


def get_user_by_username(uow: AbstractUow, username: str) -> Optional[User]:
    with uow:
        return uow.user.get_by_username(username)


def create_new_user(uow: AbstractUow, user: User, current_user: User):
    if (
        user.permission.value >= Permissions.table.value
        and current_user.permission.value < Permissions.vice_president.value
    ):
        raise HTTPException(
            status_code=401,
            detail="Você não possui permissão para cadastrar um usuário da mesa.",
        )

    if (
        user.permission == Permissions.president.value
        and current_user.permission < Permissions.root.value
    ):
        raise HTTPException(
            status_code=401,
            detail="Você não possui permissão para cadastrar um usuário Presidente.",
        )

    if current_user.permission.value < Permissions.table.value:
        raise HTTPException(status_code=401, detail="Você não pode criar um usuário.")

    with uow:
        user.password = hash_password(user.password)
        uow.user.add(user)


def verify_if_user_exists(uow: AbstractUow, user: User):
    user_created = get_user_by_email(uow, user.email)
    if user_created:
        if user_created.email == user.email:
            return True

    return False


# TODO: Create a service to update user
def update_user():
    pass


# TODO: Create a service to delete user
def delete(uow: AbstractUow, user_id: UUID):
    with uow:
        uow.user.remove(user_id)


def get(uow: AbstractUow):
    with uow:
        yield from uow.user.iter()


def change_user(user: User | ModelUser) -> ModelUser | User:
    if type(user) == User:
        return ModelUser(
            credentials=Credentials(
                username=user.username, email=user.email, password=user.password
            ),
            permission=user.permission,
            hub=user.hub,
            src_profile=user.src_profile,
            fk_band=user.fk_band,
        )
    return User(
        username=user.credentials.username,
        email=user.credentials.email,
        password=user.credentials.password,
        permission=user.permission,
        hub=user.hub,
        src_profile=user.src_profile,
        fk_band=user.fk_band,
    )
