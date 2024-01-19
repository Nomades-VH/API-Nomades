from fastapi import APIRouter, Depends

from app.auth.services import get_current_user_with_permission
from app.kibon_donjak import services as sv
from app.kibon_donjak.models import KibonDonjak
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.controllers.create_controller import create_controller
from app.utils.controllers.get_controller import get_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/kibon_donjak")


# TODO: Create Get method
@router.get("/")
@get_controller(sv)
async def get(
        message_error: str = "Não foram encontrados kibon donjaks.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
):
    ...


# TODO: Create Get Method
@router.get("/")
async def get_by_id():
    pass


# TODO: Create Post Method
@router.post("/")
@create_controller(sv)
async def post(
        model: KibonDonjak,
        message_error: str = "Não foi possível criar Kinbo Don Jak.",
        message_success: str = "Kinbo criado com sucesso.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
):
    ...


# TODO: Create Put Method
@router.put("/")
async def put():
    pass


# TODO: Create Delete Method
@router.delete("/")
async def delete():
    pass
