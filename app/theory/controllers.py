from dataclasses import asdict
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends

from app.auth.services import get_current_user_with_permission
from app.theory.models import Theory as ModelTheory
from app.theory import services as sv
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.utils.delete_controller import delete_controller
from general_enum.permissions import Permissions
from ports.uow import AbstractUow

router = APIRouter(prefix="/theory")


# TODO: Review methods get_theories, post and get
@router.get("/")
async def get_theories(
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> List[dict]:
    return list(map(asdict, sv.get_all_theories(uow)))


@router.post("/")
async def post_theory(
        model: ModelTheory, uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.vice_president))
) -> None:
    sv.add_theory(uow, model)


@router.get("/{theory_id}")
async def get_theory(
    theory_id: UUID, uow: AbstractUow = Depends(SqlAlchemyUow),
    current_user: User = Depends(get_current_user_with_permission(Permissions.student))
) -> Optional[dict]:
    return asdict(sv.get_by_id(uow, theory_id))


# TODO: Create Put Method
@router.put("/")
async def put_theory():
    ...


@router.delete("/{id}")
@delete_controller(sv)
async def delete_theory(
        uuid: UUID,
        message_success: str = "A teoria foi deletada com sucesso.",
        message_error: str = "A teoria não foi encontrada.",
        uow: AbstractUow = Depends(SqlAlchemyUow),
        current_user: User = Depends(get_current_user_with_permission(Permissions.president))
):
    ...
