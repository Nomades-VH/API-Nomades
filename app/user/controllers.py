from dataclasses import asdict

from fastapi import APIRouter, Depends, HTTPException

from app.auth.services import get_current_user
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.user.models import User as ModelUser
from app.user.exceptions import EmailAlreadyExists
from app.user.services import create_new_user, get_user_by_email, change_user, get_user_by_username, \
    verify_if_user_exists
from ports.uow import AbstractUow

router = APIRouter(prefix="/user")


# TODO: Verify methods
@router.post("/")
async def create_user(user: ModelUser, uow: AbstractUow = Depends(SqlAlchemyUow)) -> None:
    try:
        user = change_user(user)
        verify_if_user_exists(uow, user)
        return create_new_user(uow, user)
    except EmailAlreadyExists:
        raise EmailAlreadyExists()


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return asdict(current_user)


# TODO: Create Get Method
async def get_users():
    pass


# TODO: Create Update Method
async def update_user():
    pass


# TODO: Create Delete Method
async def delete_user():
    pass
