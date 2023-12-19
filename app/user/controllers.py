from dataclasses import asdict
from typing import Optional

from fastapi import APIRouter, Depends

from app.auth.services import get_current_user, get_current_user_with_permission
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.user.exceptions import UserException
from app.user.models import User as ModelUser
from app.user import services as sv
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/user")


# TODO: Verify methods
@router.post("/")
async def create_user(
        user: ModelUser,
        current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
) -> Optional[dict]:
    try:
        user = sv.change_user(user)
        sv.verify_if_user_exists(uow, user)
        sv.create_new_user(uow, user, current_user)
        return {'user': user.id}
    except UserException as e:
        return {'status': e.status_code, 'message': e.message}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return asdict(current_user)


# TODO: Create Get Method

@router.get('/')
async def get_users(
        current_user: User = Depends(get_current_user_with_permission(Permissions.vice_president)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    return list(map(asdict, sv.get_all_users(uow)))


# TODO: Create Update Method
async def update_user(
        current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    pass


# TODO: Create Delete Method
async def delete_user():
    pass
