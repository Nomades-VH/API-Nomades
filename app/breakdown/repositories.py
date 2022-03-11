from abc import ABC
from typing import Iterator, Optional
from uuid import UUID

from app.breakdown.entities import Breakdown
from ports.repository import AbstractRepository


class AbstractBreakdownRepository(AbstractRepository[Breakdown], ABC):
    pass


class BreakdownRepository(AbstractBreakdownRepository):

    def get(self, id: UUID) -> Optional[Breakdown]:
        return self.session.query(Breakdown).filter(Breakdown.id == id).first()

    def add(self, breakdown: Breakdown) -> None:
        self.session.add(breakdown)

    def remove(self, uuid: UUID) -> Optional[Breakdown]:
        return self.session.query(Breakdown).filter(Breakdown.id == uuid).delete()

    def update(self, breakdown: Breakdown) -> None:
        self.session.query(Breakdown).filter(Breakdown.id == breakdown.id).update(breakdown)

    def iter(self) -> Iterator[Breakdown]:
        return self.session.query(Breakdown).all()
