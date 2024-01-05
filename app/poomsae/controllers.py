from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Response

from app.auth.services import get_current_user_with_permission
from app.poomsae import services as poomsae_sv
from app.poomsae.entities import Poomsae as PoomsaeEntity
from app.poomsae.models import Poomsae
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.create_controller import create_controller
from app.utils.get_controller import get_controller
from app.utils.update_controller import update_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/poomsae")


# TODO: Create Get Method
@router.get("/")
@get_controller(poomsae_sv)
async def get_all(
        message_error: str = "Não foi possível encontrar os poomsaes.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
) -> Response:
    ...


# TODO: Create Get Method
@router.get("/{poomsae_id}")
async def get_poomsae():
    pass


# TODO: Create Post Method
@router.post("/")
@create_controller(poomsae_sv)
async def create_poomsae(
        model: Poomsae,
        message_success: str = "Poomsae criado com sucesso.",
        message_error: str = "Não foi possível criar o Poomsae.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
) -> Response:
    ...


# TODO: Create Put Method
@router.put("/{id}")
@update_controller(poomsae_sv)
async def update_poomsae(
        id: UUID,
        model: Poomsae,
        message_success: str = "Poomsae atualizado com sucesso.",
        message_error: str = "Não foi possível atualizar o Poomsae.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
):
    ...


# TODO: Create Delete Method
@router.delete("/")
async def delete_poomsae():
    pass
