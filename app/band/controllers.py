from dataclasses import asdict
from typing import Optional, List
from uuid import UUID

from fastapi import APIRouter, Depends

from app.band.models import Band
from app.band.services import get_all_bands, get_band_by_id, add_band, make_band
from app.uow import SqlAlchemyUow
from ports.uow import AbstractUow

router = APIRouter(prefix="/band")


@router.get("/")
async def get_bands(uow: AbstractUow = Depends(SqlAlchemyUow)) -> List[dict]:
    return list(map(asdict, get_all_bands(uow)))


@router.post("/")
async def add_new_band(model: Band, uow: AbstractUow = Depends(SqlAlchemyUow)) -> None:
    band = make_band(model)
    add_band(uow, band)


@router.get("/{band_id}")
async def get_band(band_id: UUID, uow: AbstractUow = Depends(SqlAlchemyUow)) -> Optional[dict]:
    return asdict(get_band_by_id(uow, band_id))
