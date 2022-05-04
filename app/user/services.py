from uuid import UUID

from fastapi import HTTPException
from passlib.context import CryptContext

from app.auth.hasher import hash_password
from app.user.entities import User
from app.user.models import User as UserModel


# TODO: Method GET Itens abaixo
from ports.uow import AbstractUow

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user_by_id(uow: AbstractUow, user_id: UUID) -> User:
    with uow:
        return uow.user.get(user_id)


def get_user_by_email(uow: AbstractUow, email: str) -> User:
    with uow:
        return uow.user.get_by_email(email)


def create_new_user(uow: AbstractUow, username: str, email: str, password: str, fk_band: UUID) -> UserModel:
    user = get_user_by_email(uow, email)

    if user is not None:
        raise HTTPException(status_code=400, detail="User already registered")

    with uow:
        user = User(
            username=username,
            email=email,
            password=hash_password(password),
            fk_band=fk_band,
        )

        uow.user.add(user)

        user = make_user_model(user)
        return user


def make_user_model(user: User) -> UserModel:
    return UserModel(
        username=user.username,
        email=user.email,
        password=user.password,
        fk_band=user.fk_band,
    )
