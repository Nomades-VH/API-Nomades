from dataclasses import asdict
from typing import List, Any

from fastapi import APIRouter, Depends, HTTPException

from app.auth.services import get_current_user_with_permission
from app.poomsae import services as poomsae_sv
from app.poomsae.entities import Poomsae
from app.poomsae.models import Poomsae
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.create_controller import create_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/poomsae")


# TODO: Create Get Method
@router.get("/")
async def get_all(uow: AbstractUow = Depends(SqlAlchemyUow)) -> List[dict]:
    return list(map(asdict, poomsae_sv.get_all_poomsaes(uow)))


# TODO: Create Get Method
@router.get("/{poomsae_id}")
async def get_poomsae():
    pass


# TODO: Create Post Method
@router.post("/")
@create_controller(poomsae_sv)
async def create_poomsae(
        entity: Poomsae,
        message_success: str = "Poomsae criado com sucesso.",
        message_error: str = "Não foi possível criar um Poomsae.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.vice_president))
):
    ...


# TODO: Create Put Method
@router.put("/")
async def update_poomsae():
    pass


# TODO: Create Delete Method
@router.delete("/")
async def delete_poomsae():
    pass
