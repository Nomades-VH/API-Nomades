from dataclasses import asdict
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from app.theory.models import Theory as ModelTheory
from app.theory.services import get_all_theories, add_theory, get_theory_by_id
from app.uow import SqlAlchemyUow
from ports.uow import AbstractUow

router = APIRouter(prefix="/theory")


# TODO: Review methods get_theories, post and get
@router.get("/")
async def get_theories(uow: AbstractUow = Depends(SqlAlchemyUow)) -> List[dict]:
    return list(map(asdict, get_all_theories(uow)))


@router.post("/")
async def post_theory(model: ModelTheory, uow: AbstractUow = Depends(SqlAlchemyUow)) -> None:
    add_theory(uow, model)


@router.get("/{theory_id}")
async def get_theory(
    theory_id: UUID, uow: AbstractUow = Depends(SqlAlchemyUow)
) -> Optional[dict]:
    return asdict(get_theory_by_id(uow, theory_id))


# TODO: Create Put Method
@router.put("/")
async def put_theory():
    pass


# TODO: Create Delete Method
@router.delete("/")
async def delete_theory():
    pass
