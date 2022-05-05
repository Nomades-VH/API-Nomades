from abc import ABC

from app.theory.entities import Theory
from typing import Optional, Iterator
from uuid import UUID

from ports.repository import AbstractRepository


class AbstractTheoryRepository(AbstractRepository[Theory], ABC):
    pass


class TheoryRepository(AbstractTheoryRepository):
    def get(self, uuid: UUID) -> Optional[Theory]:
        return self.session.query(Theory).filter(Theory.id == uuid).first()

    def add(self, theory: Theory) -> None:
        self.session.add(theory)

    def update(self, theory: Theory) -> None:
        self.session.query(Theory).filter(Theory.id == theory.id).update(theory)

    def remove(self, uuid: UUID) -> Optional[Theory]:
        return self.session.query(Theory).filter(Theory.id == uuid).delete()

    def iter(self) -> Iterator[Theory]:
        return self.session.query(Theory).all()
