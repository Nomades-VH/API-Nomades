from functools import wraps
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import Response
from starlette.responses import JSONResponse

from app.auth.services import get_current_user_with_permission
from app.band.models import Band
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.controllers.create_controller import create_controller
from app.utils.controllers.delete_controller import delete_controller
from app.utils.controllers.get_by_controller import get_by_controller
from app.utils.controllers.get_controller import get_controller
from app.utils.controllers.update_controller import update_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow
from app.band import services as sv

router = APIRouter(prefix="/band")


# TODO: Arrumar essas verificações, está muito amador


@router.get("/")
@get_controller(sv)
async def get(
        message_error: str = "Não foram encontradas faixas.",
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
        uow: AbstractUow = Depends(SqlAlchemyUow),
) -> Response:
    ...


@router.get("/me")
async def get_my_band(
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
        uow: AbstractUow = Depends(SqlAlchemyUow),
):
    band = sv.get_by_user(uow, current_user)
    if not band:
        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={
                "message": "Você não tem uma faixa."
            }
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content=jsonable_encoder(band)
    )


@router.get("/{param}")
@get_by_controller(sv.get_by_id, '')
async def get_by_id(
        param: UUID,
        message_error: str = "Faixa não encontrada.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> Response:
    ...


@router.get("/gub/{param}")
@get_by_controller(sv.get_by_gub, '')
async def get_by_gub(
        param: int,
        message_error: str = "Faixa não encontrada.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
) -> Response:
    band = sv.get_by_user(uow, current_user)

    if band and current_user.permission.value < Permissions.table.value and band.gub > param:
        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={
                "message": "Você ainda não chegou nessa faixa."
            }
        )


@router.post("/")
@create_controller(sv)
async def post(
        model: Band,
        message_success: str = "Faixa criada com sucesso.",
        message_error: str = "Erro ao criar a faixa.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(
            get_current_user_with_permission(Permissions.table)
        )
) -> Response:
    if sv.get_by_gub(uow, model.gub):
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"message": f"Gub {model.gub} já existe."}
        )


@router.put("/{uuid}")
@update_controller(sv)
async def put(
        uuid: UUID,
        model: Band,
        message_success: str = "Faixa atualizada.",
        message_error: str = "Faixa não atualizada.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(
            get_current_user_with_permission(Permissions.table)
        )
):
    ...


@router.post('/{uuid_band}/kick')
async def add_kicks(
        uuid_band: UUID,
        kicks: Optional[List[UUID]],
        uow: AbstractUow = Depends(SqlAlchemyUow),
        message_error: str = "Não foi possível inserir chutes.",
        message_success: str = "Chutes adicionados com sucesso.",
        current_user: User = Depends(
            get_current_user_with_permission(Permissions.table)
        )
):
    return add_item(uuid_band=uuid_band, items=kicks, uow=uow, current_user=current_user, message_error=message_error,
                    message_success=message_success, service_add=sv.add_kicks)


@router.post('/{uuid_band}/poomsae')
async def add_poomsaes(
        uuid_band: UUID,
        poomsaes: Optional[List[UUID]],
        message_error: str = "Não foi possível adicionar poomsaes.",
        message_success: str = "Poomsaes adicionados a faixa com sucesso.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(
            get_current_user_with_permission(Permissions.table)
        )
):
    return add_item(
        uuid_band=uuid_band,
        items=poomsaes,
        uow=uow,
        current_user=current_user,
        message_error=message_error,
        message_success=message_success,
        service_add=sv.add_poomsaes
    )


@router.post('/{uuid_band}/kibon_donjak')
async def add_kibon_donjak(
        uuid_band: UUID,
        kibon_donjak: Optional[List[UUID]],
        message_error: str = "Não foi possível adicionar kibon_donjaks",
        message_success: str = "Kibon Donjaks adicionados a faixa com sucesso.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(
            get_current_user_with_permission(Permissions.table)
        )
):
    return add_item(
        uuid_band=uuid_band,
        items=kibon_donjak,
        uow=uow,
        current_user=current_user,
        message_error=message_error,
        message_success=message_success,
        service_add=sv.add_kibon_donjaks
    )


def add_item(
        uuid_band: UUID,
        items: Optional[List[UUID]],
        message_error: str,
        message_success: str,
        service_add,
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(
            get_current_user_with_permission(Permissions.table)
        )
):
    response = service_add(uuid_band, items, uow)

    if response is None:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"message": message_error}
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": message_success}
    )


def delete_item(uuid_band: UUID,
                uuid_item: UUID,
                message_error: str,
                message_success: str,
                service_delete,
                uow: AbstractUow,
                current_user: User
                ):
    response = service_delete(uuid_band, uuid_item, uow)

    if response is None:
        return JSONResponse(
            status_code=HTTPStatus.NOT_FOUND,
            content={"message": message_error}
        )

    return JSONResponse(
        status_code=HTTPStatus.OK,
        content={"message": message_success, "id": jsonable_encoder(response)}
    )


@router.delete('/{uuid_band}/kick/{uuid_kick}')
async def delete_kick(
        uuid_band: UUID,
        uuid_kick: UUID,
        message_error="Faixa ou chute não encontrada.",
        message_success="Chute retirado da faixa com sucesso.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(
            get_current_user_with_permission(Permissions.table)
        )
):
    return delete_item(uuid_band=uuid_band, uuid_item=uuid_kick, message_error=message_error,
                       message_success=message_success, service_delete=sv.delete_kick, uow=uow,
                       current_user=current_user)


@router.delete('/{uuid_band}/poomsae/{uuid_poomsae}')
async def delete_poomsae(
        uuid_band: UUID,
        uuid_poomsae: UUID,
        message_error="Faixa ou Poomsae não encontrado.",
        message_success="Poomsae retirado da faixa com sucesso.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(
            get_current_user_with_permission(Permissions.table)
        )
):
    return delete_item(uuid_band=uuid_band, uuid_item=uuid_poomsae, message_error=message_error,
                       message_success=message_success, service_delete=sv.delete_poomsae, uow=uow,
                       current_user=current_user)


@router.delete('/{uuid_band}/kibon_donjak/{uuid_kibon_donjak}')
async def delete_kibon_donjak(
        uuid_band: UUID,
        uuid_kibon_donjak: UUID,
        message_error: str = "Faixa ou Kibon Donjak não encontrado.",
        message_success="Kibon Donjak retirado da faixa com sucesso.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(
            get_current_user_with_permission(Permissions.table)
        )
):
    return delete_item(uuid_band=uuid_band, uuid_item=uuid_kibon_donjak, message_error=message_error,
                       message_success=message_success, service_delete=sv.delete_kibon_donjak, uow=uow,
                       current_user=current_user)


@router.delete("/{uuid}")
@delete_controller(sv)
async def delete(
        uuid: UUID,
        message_success: str = "Faixa deletada.",
        message_error: str = "Faixa não encontrada.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
) -> Response:
    ...
