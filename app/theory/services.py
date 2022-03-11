from typing import Iterator
from uuid import UUID

from app.theory.entities import Theory
from app.theory.models import Theory as ModelTheory
from ports.uow import AbstractUow


def get_all_theories(uow: AbstractUow) -> Iterator[Theory]:
    with uow:
        return uow.theory.iter()


def add_theory(uow: AbstractUow, model: ModelTheory) -> None:
    with uow:
        theory = make_theory(model)
        uow.theory.add(theory)


def get_theory_by_id(uow: AbstractUow, id: UUID) -> Theory:
    with uow:
        return uow.theory.get(id)


def make_theory(model_theory: ModelTheory) -> Theory:
    return Theory(description=model_theory.description)
