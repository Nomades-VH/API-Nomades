from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import Response
from starlette.responses import JSONResponse

from app.auth.services import get_current_user_with_permission
from app.band.models import Band
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.create_controller import create_controller
from app.utils.delete_controller import delete_controller
from app.utils.get_all_controller import get_all_controller
from app.utils.get_by_controller import get_by_controller
from app.utils.update_controller import update_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow
from app.band import services as sv

router = APIRouter(prefix="/band")


@router.get("/")
@get_all_controller(sv)
async def get(
        message_error: str = "Não foi possível encontrar as faixas.",
        current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
        uow: AbstractUow = Depends(SqlAlchemyUow),
) -> Response:
    ...


@router.get("/me/")
async def get_my_band(
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
        uow: AbstractUow = Depends(SqlAlchemyUow),
):
    if current_user.fk_band is None:
        raise HTTPException(
            status_code=401, detail="You need a band to access this resource"
        )

    band = sv.get_by_id(uow, current_user.fk_band)

    if current_user.fk_band != band.id:
        raise HTTPException(
            status_code=401, detail="You are not authorized to access this resource"
        )

    return band


@router.get("/{param}")
@get_by_controller(sv.get_by_id)
async def get_by_id(
        param: UUID,
        message_error: str = "Faixa não encontrada.",
        current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
        uow: AbstractUow = Depends(SqlAlchemyUow),
) -> Response:
    # TODO: Bloquear para que o estudante não possa pegar faixas diferentes da dele ou anteriores.
    ...


@router.get("/gub/{param}")
@get_by_controller(sv.get_by_gub)
async def get_by_gub(
        param: int,
        uow: AbstractUow = Depends(SqlAlchemyUow),
        message_error: str = "Faixa não encontrada.",
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
) -> Response:
    # TODO: não estou recebdo o usuário aqui
    if current_user.fk_band:
        band = sv.get_by_user(uow, current_user)

        if band.gub > param and current_user.permission.value < Permissions.table.value:
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
            get_current_user_with_permission(Permissions.president)
        )
) -> Response:
    if sv.get_by_gub(uow, model.gub) is not None:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"message": f"A faixa com o gub {model.gub} já existe."}
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


@router.delete("/{uuid}")
@delete_controller(sv)
async def delete(
        uuid: UUID,
        message_success: str = "Faixa deletada.",
        message_error: str = "Faixa não encontrada.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.president))
) -> Response:
    ...
