from abc import ABC
from typing import Optional, Iterator
from uuid import UUID

from app.stretching.entities import Stretching
from ports.repository import AbstractRepository


class AbstractStretchingRepository(AbstractRepository[Stretching], ABC):
    pass


class StretchingRepository(AbstractStretchingRepository):

    def get(self, uuid: UUID) -> Optional[Stretching]:
        return self.session.query(Stretching).filter(Stretching.id == uuid).first()

    def add(self, stretching: Stretching) -> None:
        self.session.add(stretching)

    def update(self, stretching: Stretching) -> None:
        self.session.query(Stretching).filter(Stretching.id == stretching.id).update(stretching)

    def remove(self, uuid: UUID) -> Optional[Stretching]:
        return self.session.query(Stretching).filter(Stretching.id == uuid).delete()

    def iter(self) -> Iterator[Stretching]:
        return self.session.query(Stretching).all()
