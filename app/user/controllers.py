from dataclasses import asdict
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from app.auth.services import get_current_user, get_current_user_with_permission
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.user.exceptions import UserException
from app.user.models import User as ModelUser
from app.user import services as sv
from app.utils.delete_controller import delete_controller
from app.utils.get_all_controller import get_all_controller
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
        print(user)
        sv.verify_if_user_exists(uow, user)
        sv.create_new_user(uow, user, current_user)
        return {'user': user.id}
    except UserException as e:
        return {'status': e.status_code, 'message': e.message}


@router.get("/me")
async def get_me(current_user: User = Depends(get_current_user)):
    return asdict(current_user)


# TODO: Update Get Method
@router.get('/')
@get_all_controller(sv)
async def get(
        message_error: str = "Não foi possível pegar os usuários",
        current_user: User = Depends(get_current_user_with_permission(Permissions.vice_president)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    ...


# TODO: Create Update Method
async def update_user(
        current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    pass


# TODO: Create Delete Method
@router.delete('/{uuid}')
@delete_controller(sv)
async def delete_user(
        uuid: UUID,
        message_success: str = "Usuário deletado com sucesso.",
        message_error: str = "Não foi possível deletar o usuário.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
):
    ...
