from uuid import UUID
from fastapi import APIRouter, Depends
from starlette.responses import Response
from app.auth.services import get_current_user_with_permission
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.controllers.create_controller import create_controller
from app.kick import services as sv
from app.kick.models import Kick
from app.utils.controllers.delete_controller import delete_controller
from app.utils.controllers.get_by_controller import get_by_controller
from app.utils.controllers.get_controller import get_controller
from app.utils.controllers.update_controller import update_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/kick")


@router.get("/")
@get_controller(sv)
async def get(
        message_error: str = "Não foram encontrados chutes.",
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
) -> Response:
    ...


# TODO: Create Get Method
@router.get("/{param}")
@get_by_controller(sv.get_by_id, 'kicks')
async def get_by_id(
        param: UUID,
        message_error: str = "Não foi possível encontrar esse chute",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> Response:
    ...


@router.get('/name/{param}')
@get_by_controller(sv.get_by_name, 'kicks')
async def get_by_name(
        param: str,
        message_error: str = "Não foi possível encontrar esse chute",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> Response:
    ...


# TODO: Create Post Method
@router.post("/")
@create_controller(sv)
async def post(
        model: Kick,
        message_success: str = "Chute criado.",
        message_error: str = "Chute não criado.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
) -> Response:
    ...


# TODO: Create Put Method
@router.put("/{uuid}")
@update_controller(sv)
async def put(
        uuid: UUID,
        model: Kick,
        message_success: str = "Chute atualizado com sucesso.",
        message_error: str = "Não foi possível atualizar o chute.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
) -> Response:
    ...


# TODO: Create Delete Method
@router.delete("/{uuid}")
@delete_controller(sv)
async def delete(
        uuid: UUID,
        message_success: str = "Chute deletado com sucesso.",
        message_error: str = "Não foi possivel deletar o chute.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
) -> Response:
    ...
