from dataclasses import asdict
from http import HTTPStatus
from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, FastAPI
from fastapi import Response
from starlette.responses import JSONResponse

from app.auth.services import get_current_user_with_permission
from app.band.models import Band
from app.band.entities import Band as BandEntity
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.create_controller import create_controller
from app.utils.delete_controller import delete_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow
from app.band import services as sv

app = FastAPI()

router = APIRouter(prefix="/band")


@router.get("/")
async def get_all(
        current_user: User = Depends(get_current_user_with_permission(Permissions.table)),
        uow: AbstractUow = Depends(SqlAlchemyUow),
) -> List[dict]:
    return list(map(asdict, sv.get_all(uow)))


@router.get("/{band_id}")
async def get_by_id(
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
        uow: AbstractUow = Depends(SqlAlchemyUow),
) -> dict:
    if current_user.fk_band is None:
        raise HTTPException(
            status_code=401, detail="You need a band to access this resource"
        )

    band = sv.get_by_id(uow, current_user.fk_band)

    if current_user.fk_band != band.id:
        raise HTTPException(
            status_code=401, detail="You are not authorized to access this resource"
        )

    return asdict(band)


@router.get("/gub/{gub}")
async def get_by_gub(
        gub: int,
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student)),
):
    if sv.get_by_gub(uow, gub) is None:
        raise HTTPException(
            status_code=404, detail=f"Band with gub '{gub}' does not exist"
        )

    user_band: BandEntity = sv.get_by_user(uow, current_user)

    if user_band.gub > gub and current_user.permission < Permissions.table.value:
        raise HTTPException(
            status_code=401,
            detail=f"You are not authorized to access this resource: expected gub less then {gub}, but got {user_band.gub}",
        )

    return asdict(sv.get_by_gub(uow, gub))


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
):
    if sv.get_by_gub(uow, model.gub) is not None:
        return JSONResponse(
            status_code=HTTPStatus.BAD_REQUEST,
            content={"message": f"A faixa com o gub {model.gub} já existe."}
        )


# TODO: Create Put method
@router.put("/")
async def put(
        band: Band, current_user:
        User = Depends(
            get_current_user_with_permission(Permissions.president)
        ),
        uow: AbstractUow = Depends(SqlAlchemyUow)
) -> None:
    band_actually = sv.get_by_name(uow, band.name)
    if band_actually is None:
        return

    sv.update(uow=uow, band=band)


# TODO: Create Delete method
@router.delete("/{uuid}")
@delete_controller(sv)
async def delete(
        uuid: UUID,
        message_success: str = "A faixa foi deletada com sucesso.",
        message_error: str = "A faixa não foi encontrada.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.president))
) -> Response:
    ...
