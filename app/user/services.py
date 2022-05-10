from typing import Optional
from uuid import UUID

from fastapi import HTTPException

from app.auth.hasher import hash_password
from app.auth.schemas import Credentials
from app.user.entities import User
from app.user.models import User as ModelUser
from ports.uow import AbstractUow


# TODO: Verify if this is necessary
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(uow: AbstractUow, user_id: UUID) -> Optional[User]:
    with uow:
        return uow.user.get(user_id)


def get_user_by_email(uow: AbstractUow, email: str) -> Optional[User]:
    with uow:
        return uow.user.get_by_email(email)


def get_user_by_username(uow: AbstractUow, username: str) -> Optional[User]:
    with uow:
        return uow.user.get_by_username(username)


def create_new_user(uow: AbstractUow, user: User) -> None:
    with uow:
        user.password = hash_password(user.password)
        uow.user.add(user)


def verify_if_user_exists(uow: AbstractUow, user: User):
    user_created = get_user_by_email(uow, user.email)
    if user_created:
        if user_created.email == user.email:
            raise HTTPException(status_code=400, detail=f"User with email '{user.email}' already exists")

    user_created = get_user_by_username(uow, user.username)
    if user_created:
        if user_created.username == user.username:
            raise HTTPException(status_code=400, detail=f"User with username '{user.username}' already exists")


# TODO: Create a service to update user
def update_user():
    pass


# TODO: Create a service to delete user
def delete_user():
    pass


# TODO: Create a service to get all users
def get_all_users():
    pass


def change_user(user: User | ModelUser) -> ModelUser | User:
    if type(user) == User:
        return ModelUser(
            username=user.username,
            credentials=Credentials(email=user.email, password=user.password),
            permission=user.permission,
            fk_band=user.fk_band,
        )
    return User(
        username=user.username,
        email=user.credentials.email,
        password=user.credentials.password,
        permission=user.permission.value,
        fk_band=user.fk_band,
    )
