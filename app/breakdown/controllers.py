from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.breakdown.models import Breakdown as BreakdownModel
from app.breakdown.services import get_all_breakdowns, get_breakdown_by_id, add_breakdown, add_band_breakdown, \
    make_model_breakdown
from app.uow import SqlAlchemyUow
from ports.uow import AbstractUow

router = APIRouter(prefix="/breakdown")


@router.get("/")
async def get_breakdowns(uow: AbstractUow = Depends(SqlAlchemyUow)) -> List[BreakdownModel]:
    try:
        return list(map(make_model_breakdown, get_all_breakdowns(uow)))
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
async def get_breakdown(id: UUID, uow: AbstractUow = Depends(SqlAlchemyUow)) -> Optional[BreakdownModel] | HTTPException:
    try:
        return get_breakdown_by_id(id, uow)
    # TODO: Change to BreakdownNotFoundException but I don't know how to do that
    except Exception:
        raise HTTPException(status_code=404, detail="Breakdown not found")


@router.put("/{id}")
#TODO: Make function put_breakdown
async def put_breakdown(id: UUID, model: BreakdownModel, uow: AbstractUow = Depends(SqlAlchemyUow)) -> None:
    pass