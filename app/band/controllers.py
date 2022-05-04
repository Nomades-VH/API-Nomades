from dataclasses import asdict
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from app.auth.services import get_current_user, get_current_user_with_permission
from app.band.models import Band
from app.band.services import get_all_bands, get_band_by_id, add_band, make_band
from app.uow import SqlAlchemyUow
from app.user.entities import User
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/band")


@router.get("/")
async def get_bands(current_user: User = Depends(get_current_user_with_permission(Permissions.student)), uow: AbstractUow = Depends(SqlAlchemyUow)) -> List[dict]:

    bands = list(map(asdict, get_all_bands(uow)))
    # band_atual = get_band_by_id(uow, current_user.fk_band)
    aux = []
    for band in bands:
        if current_user.permission > Permissions.table.value:
            aux.append(band)

    return aux


@router.post("/")
async def add_new_band(band_model: Band, current_user: User = Depends(get_current_user_with_permission(Permissions.president)), uow: AbstractUow = Depends(SqlAlchemyUow)) -> None:
    band = make_band(band_model)
    add_band(uow, band)


@router.get("/{band_id}")
async def get_band(current_user: User = Depends(get_current_user_with_permission(Permissions.student)), uow: AbstractUow = Depends(SqlAlchemyUow)) -> Optional[dict]:

    if current_user.fk_band is None:
        raise HTTPException(status_code=401, detail="You need a band to access this resource")

    band = get_band_by_id(uow, current_user.fk_band)

    if current_user.fk_band != band.id:
        raise HTTPException(status_code=401, detail="You are not authorized to access this resource")

    return asdict(get_band_by_id(uow, current_user.fk_band))
