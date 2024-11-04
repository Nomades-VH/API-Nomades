from uuid import UUID

from fastapi import APIRouter, Depends
from starlette.responses import Response

from app.auth.services import get_current_user_with_permission
from app.kibon_donjak import services as sv
from app.kibon_donjak.models import KibonDonjak
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.controllers.create_controller import create_controller
from app.utils.controllers.delete_controller import delete_controller
from app.utils.controllers.get_by_controller import get_by_controller
from app.utils.controllers.get_controller import get_controller
from app.utils.controllers.update_controller import update_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/kibon_donjak")


@router.get("/")
@get_controller(sv)
async def get(
    message_error: str = "Não foram encontrados kibon donjaks.",

    current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
    uow: AbstractUow = Depends(SqlAlchemyUow),
) -> Response: ...


@router.get("/{param}")
@get_by_controller(sv.get_by_id, "kibon_donjaks")
async def get_by_id(
    param: UUID,
    message_error: str = "Não foi possível encontrar esse Kibon Donjak",
    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
) -> Response: ...


@router.get("/band/{param}")
@get_by_controller(sv.get_by_band, "kibon_donjaks")
async def get_by_band(
    param: UUID,
    message_error: str = "Não foi possível encontrar os Kibon Donjaks dessa faixa.",
    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
) -> Response: ...


@router.post("/")
@create_controller(sv)
async def post(
    model: KibonDonjak,
    message_error: str = "Não foi possível criar Kinbo DonJak.",
    message_success: str = "Kibon Donjak criado com sucesso.",
    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
) -> Response: ...


@router.put("/{uuid}")
@update_controller(sv)
async def put(
    uuid: UUID,
    model: KibonDonjak,
    message_success: str = "Kibon Donjak atualizado com sucesso.",
    message_error: str = "Não foi possível atualizar o Kibon Donjak.",
    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
) -> Response: ...


@router.delete("/{uuid}")
@delete_controller(sv)
async def delete(
    uuid: UUID,
    message_success: str = "Kibon Donjak deletado com sucesso.",
    message_error: str = "Não foi possível deletar esse Kibon Donhak",

    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
) -> Response: ...
