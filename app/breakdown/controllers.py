from dataclasses import asdict
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.breakdown.models import Breakdown as BreakdownModel
from app.breakdown.services import get_all_breakdowns, get_breakdown_by_id, add_breakdown, add_band_breakdown, \
    update_breakdown, remove_breakdown
from app.uow import SqlAlchemyUow
from ports.uow import AbstractUow

router = APIRouter(prefix="/breakdown")


@router.get("/")
async def get_breakdowns(uow: AbstractUow = Depends(SqlAlchemyUow)) -> List[BreakdownModel]:
    try:
        return list(map(asdict, get_all_breakdowns(uow)))
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")


@router.post("/{band_id}")
async def post_breakdown(band_id: UUID, model: BreakdownModel, uow: AbstractUow = Depends(SqlAlchemyUow)) -> None:
    try:
        breakdown_id = add_breakdown(model, uow)
        add_band_breakdown(band_id, breakdown_id, uow)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")


@router.get("/{id}")
async def get_breakdown(id: UUID, uow: AbstractUow = Depends(SqlAlchemyUow)) -> Optional[dict] | HTTPException:
    try:
        return asdict(get_breakdown_by_id(id, uow))

    # TODO: Change to BreakdownNotFoundException but I don't know how to do that
    except Exception:
        raise HTTPException(status_code=404, detail="Breakdown not found")


@router.put("/{id}")
async def put_breakdown(breakdown_id: UUID, model: BreakdownModel, uow: AbstractUow = Depends(SqlAlchemyUow)) -> None:
    try:
        update_breakdown(breakdown_id, model, uow)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")


@router.delete("/{band_id}/{breakdown_id}")
async def delete_breakdown(band_id: UUID, breakdown_id: UUID, uow: AbstractUow = Depends(SqlAlchemyUow)) -> None:
    try:
        remove_breakdown(band_id, breakdown_id, uow)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")
