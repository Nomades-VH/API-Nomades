from dataclasses import asdict
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from app.auth.services import get_current_user_with_permission
from app.breakdown.models import Breakdown as BreakdownModel
from app.breakdown import services as sv


from app.uow import SqlAlchemyUow
from app.user.entities import User
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/breakdown")


@router.get("/")
async def get(
    uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> List[dict]:
    try:
        return list(map(asdict, sv.get_all(uow)))
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")


@router.post("/{band_id}")
async def post(
    band_id: UUID, model: BreakdownModel, uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.vice_president))
) -> None:
    try:
        breakdown_id = sv.add(model, uow)
        sv.add_band_breakdown(band_id, breakdown_id, uow)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")


@router.get("/{id}")
async def get_by_id(
    id: UUID, uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> Optional[dict]:
    try:
        return asdict(sv.get_by_id(id, uow))

    except Exception:
        raise HTTPException(status_code=404, detail="Breakdown not found")


@router.put("/{id}")
async def put(
    breakdown_id: UUID, model: BreakdownModel, uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.vice_president))
) -> None:
    try:
        sv.update(breakdown_id, model, uow)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")


@router.delete("/{band_id}/{breakdown_id}")
async def delete(
    band_id: UUID, breakdown_id: UUID, uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.vice_president))
) -> None:
    try:
        sv.remove_breakdown(band_id, breakdown_id, uow)
    except Exception:
        raise HTTPException(status_code=400, detail="Bad request")
