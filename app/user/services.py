from uuid import UUID
from fastapi import HTTPException
from passlib.context import CryptContext
from app.auth.hasher import hash_password
from app.user.entities import User
from app.user.models import User as UserModel
from ports.uow import AbstractUow


# TODO: Verify if this is necessary
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(uow: AbstractUow, user_id: UUID) -> User:
    with uow:
        return uow.user.get(user_id)


def get_user_by_email(uow: AbstractUow, email: str) -> User:
    with uow:
        return uow.user.get_by_email(email)


def create_new_user(uow: AbstractUow, user: User) -> None:
    if get_user_by_email(uow, user.email) is not None:
        raise HTTPException(
            status_code=400, detail=f"User {user.username} already registered"
        )

    with uow:
        user.password = hash_password(user.password)
        uow.user.add(user)


# TODO: Create a service to update user
def update_user():
    pass


# TODO: Create a service to delete user
def delete_user():
    pass


# TODO: Create a service to get all users
def get_all_users():
    pass


def change_model_user(user: User | UserModel) -> UserModel | User:
    if type(user) == User:
        return UserModel(
            username=user.username,
            email=user.email,
            password=user.password,
            permission=user.permission,
            fk_band=user.fk_band,
        )
    return User(
        username=user.username,
        email=user.email,
        password=user.password,
        permission=user.permission.value,
        fk_band=user.fk_band,
    )
