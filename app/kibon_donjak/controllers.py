from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import Response, JSONResponse

from app.auth.services import get_current_user_with_permission
from app.kibon_donjak import services as sv
from app.band import services as sv_band
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
        uow: AbstractUow = Depends(SqlAlchemyUow)
) -> Response:
    if current_user.permission.value < Permissions.table.value:
        band = sv_band.get_by_id(uow, current_user.fk_band)
        if band:
            bands = sv_band.get_minors_band(uow, band.gub)
            kibon_donjaks = {}
            for band in bands:
                kibon_donjaks[band.name] = band.kibon_donjaks

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=jsonable_encoder(kibon_donjaks)
            )

        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={"message": "Você não possui uma faixa. Procure mais informações com seu professor."}
        )


@router.get("/{param}")
@get_by_controller(sv.get_by_id)
async def get_by_id(
        param: UUID,
        message_error: str = "Não foi possível encontrar esse Kibon Donjak",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> Response:
    if current_user.permission.value < Permissions.table.value:
        band_user = sv_band.get_by_user(uow, current_user)

        if not band_user:
            return JSONResponse(
                status_code=HTTPStatus.FORBIDDEN,
                content={"message": "Você não tem permissão para encontrar esse Kibon Don Jak."}
            )

        minors_bands = sv_band.get_minors_band(uow, band_user.gub)
        for band in minors_bands:
            for kibon_donjak in band.kibon_donjaks:
                if kibon_donjak.id == param:
                    return JSONResponse(
                        status_code=HTTPStatus.OK,
                        content=jsonable_encoder(kibon_donjak)
                    )

        return JSONResponse(
            status_code=HTTPStatus.FORBIDDEN,
            content={"message": "Você não pode acessar esse kibon_donjak"}
        )


@router.get("/band/{param}")
@get_by_controller(sv.get_by_band)
async def get_by_band(
        param: UUID,
        message_error: str = "Não foi possível encontrar os Kibon Donjaks dessa faixa.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> Response:
    ...


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


@router.put("/{uuid}")
@update_controller(sv)
async def put(
        uuid: UUID,
        model: KibonDonjak,
        message_success: str = "Kibon Donjak atualizado com sucesso.",
        message_error: str = "Não foi possível atualizar o Kibon Donjak.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
):
    ...


@router.delete("/{uuid}")
@delete_controller(sv)
async def delete(
        uuid: UUID,
        message_success: str = "Kibon Donjak deletado com sucesso.",
        message_error: str = "Não foi possível deletar esse Kibon Donhak",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.table))
):
    ...
