from fastapi import APIRouter, Depends

from app.auth.services import get_current_user_with_permission
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.controllers.create_controller import create_controller
from app.kick import services as sv
from app.kick.models import Kick
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/kick")


# TODO: Create Get Method
@router.get("/")
async def get():
    pass


# TODO: Create Get Method
@router.get("/")
async def get_by_id():
    pass


# TODO: Create Post Method
@router.post("/")
@create_controller(sv)
async def post(
        model: Kick,
        message_success: str = "Chute criado.",
        message_error: str = "Chute não criado.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
):
    pass


# TODO: Create Put Method
@router.put("/")
async def put():
    pass


# TODO: Create Delete Method
@router.delete("/")
async def delete():
    pass
