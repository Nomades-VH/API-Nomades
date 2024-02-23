from http import HTTPStatus
from uuid import UUID
from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse, Response
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
from app.band import services as sv_band

router = APIRouter(prefix="/kick")


@router.get("/")
@get_controller(sv)
async def get(
        message_error: str = "Não foram encontrados chutes.",
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
        uow: AbstractUow = Depends(SqlAlchemyUow)
):
    if current_user.permission.value < Permissions.table.value:
        try:
            band = sv_band.get_by_user(uow, current_user)
            if not band:
                return JSONResponse(
                    status_code=HTTPStatus.FORBIDDEN,
                    content={"message": "Você não possui uma faixa. Procure mais informações com seu professor."}
                )

            bands = sv_band.get_minors_band(uow, band.gub)
            kicks = {}
            for band in bands:
                if len(band.kicks) > 0:
                    kicks[band.name] = band.kicks

            return JSONResponse(
                status_code=HTTPStatus.OK,
                content=jsonable_encoder(kicks)
            )

        except Exception:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={
                    "message": "Ocorreu algum erro. Tente novamente em alguns minutos.",
                    "to_do": "Caso o problema persista, favor comunicar seu professor."
                }
            )


# TODO: Create Get Method
@router.get("/{param}")
@get_by_controller(sv.get_by_id)
async def get_by_id(
        param: UUID,
        message_error: str = "Não foi possível encontrar esse chute",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student))
):
    if current_user.permission.value < Permissions.table.value:
        try:
            band_user = sv_band.get_by_user(uow, current_user)

            if not band_user:
                return JSONResponse(
                    status_code=HTTPStatus.FORBIDDEN,
                    content={"message": "Você não tem permissão para encontrar esse Kibon Don Jak."}
                )

            minors_band = sv_band.get_minors_band(uow, band_user.gub)
            for band in minors_band:
                for kick in band.kicks:
                    if kick.id == param:
                        return JSONResponse(
                            status_code=HTTPStatus.OK,
                            content=jsonable_encoder(kick)
                        )

            return JSONResponse(
                status_code=HTTPStatus.FORBIDDEN,
                content={"message": "Você não pode acessar esse chute."}
            )
        except Exception:
            return JSONResponse(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                content={
                    "message": "Ocorreu algum erro. Tente novamente em alguns minutos.",
                    "to_do": "Caso o problema persista, favor comunicar seu professor."
                }
            )


@router.get('/name/{param}')
@get_by_controller(sv.get_by_name)
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
):
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
):
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
):
    ...
