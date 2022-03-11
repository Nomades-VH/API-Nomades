from dataclasses import asdict
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from app.theory.models import Theory as ModelTheory
from app.theory.services import get_all_theories, make_theory, add_theory, get_theory_by_id
from app.uow import SqlAlchemyUow
from ports.uow import AbstractUow

router = APIRouter(prefix="/theory")


@router.get("/")
async def get_theories(uow: AbstractUow = Depends(SqlAlchemyUow)) -> List[dict]:
    return list(map(asdict, get_all_theories(uow)))


@router.post("/")
def add_theory(model: ModelTheory, uow: AbstractUow = Depends(SqlAlchemyUow)) -> None:
    theory = make_theory(model)
    add_theory(uow, theory)


@router.get("/{theory_id}")
async def get_theory(theory_id: UUID, uow: AbstractUow = Depends(SqlAlchemyUow)) -> Optional[dict]:
    return asdict(get_theory_by_id(uow, theory_id))
