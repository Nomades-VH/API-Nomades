from dataclasses import asdict

from fastapi import APIRouter, Depends

from app.auth.services import get_current_user
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.user.exceptions import EmailAlreadyExists
from app.user.models import User as UserModel
from app.user.services import create_new_user
from ports.uow import AbstractUow

router = APIRouter(prefix="/user")


@router.post("/")
def create_user(user: UserModel, uow: AbstractUow = Depends(SqlAlchemyUow)):
    try:
        user = create_new_user(
            uow,
            user.username,
            user.email,
            user.password,
            user.fk_band
        )
    except EmailAlreadyExists:
        raise EmailAlreadyExists(user.email)


@router.get("/me")
def get_me(current_user: User = Depends(get_current_user)):
    return asdict(current_user)
