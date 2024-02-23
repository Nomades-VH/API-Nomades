from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.auth.services import get_current_user_with_permission
from app.poomsae import services as sv
from app.band import services as sv_band
from app.poomsae.models import Poomsae
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.controllers.create_controller import create_controller
from app.utils.controllers.delete_controller import delete_controller
from app.utils.controllers.get_controller import get_controller
from app.utils.controllers.update_controller import update_controller
from app.utils.controllers.get_by_controller import get_by_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/poomsae")


# TODO: Create Get Method
@router.get("/")
@get_controller(sv)
async def get(
        message_error: str = "Não foi possível encontrar os poomsaes.",
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
    uow: AbstractUow = Depends(SqlAlchemyUow),
) -> Response:
    if current_user.permission.value < Permissions.table.value:
        band = sv_band.get_by_user(uow, current_user)

        if band:
            bands = sv_band.get_minors_band(uow, band.gub)
            poomsaes = {}

            for band in bands:
                poomsaes[band.name] = band.poomsaes

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=jsonable_encoder(poomsaes)
            )

        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={"message": "Você não possui uma faixa. Procure mais informações com seu professor."}
        )


# TODO: Create Get Method
@router.get("/{param}")
@get_by_controller(sv.get_by_id)
async def get_by_id(
        param: UUID,
        message_error: str = "Não foi possível encontrar o Poomsae.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> Response:
    if current_user.permission.value < Permissions.table.value:
        band_user = sv_band.get_by_user(uow, current_user)

        if not band_user or band_user.id != param:
            return JSONResponse(
                status_code=HTTPStatus.FORBIDDEN,
                content={"message": "Você não tem permissão para acessar esse Poomsae."}
            )

        minors_band = sv_band.get_minors_band(uow, band_user.gub)
        for band in minors_band:
            for poomsae in band.poomsaes:
                if poomsae.id == param:
                    return JSONResponse(
                        status_code=HTTPStatus.OK,
                        content=jsonable_encoder(poomsae)
                    )

        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={"message": "Você não pode acessar esse Poomsae."}
        )


# TODO: Create Post Method
@router.post("/")
@create_controller(sv)
async def post(
        model: Poomsae,
        message_success: str = "Poomsae criado com sucesso.",
        message_error: str = "Não foi possível criar o Poomsae.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
) -> Response:
    ...


# TODO: Create Put Method
@router.put("/{uuid}")
@update_controller(sv)
async def put(
        uuid: UUID,
        model: Poomsae,
        message_success: str = "Poomsae atualizado com sucesso.",
        message_error: str = "Não foi possível atualizar o Poomsae.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
):
    ...


# TODO: Create Delete Method
@router.delete("/{uuid}")
@delete_controller(sv)
async def delete(
        uuid: UUID,
        message_success: str = "Poomsae deletado com sucesso.",
        message_error: str = "Não foi possível deletar o poomsae.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.president))
):
    ...
