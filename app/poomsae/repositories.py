from abc import ABC
from typing import Iterator, Optional
from uuid import UUID

from app.poomsae.entities import Poomsae
from ports.repository import AbstractRepository


class AbstractPoomsaeRepository(AbstractRepository[Poomsae], ABC):
    def get_by_name(self, name: str) -> Optional[Poomsae]:
        ...

    pass


class PoomsaeRepository(AbstractPoomsaeRepository):
    def get(self, uuid: UUID) -> Optional[Poomsae]:
        return self.session.query(Poomsae).filter(Poomsae.id == uuid).first()

    def get_by_name(self, name: str) -> Optional[Poomsae]:
        return self.session.query(Poomsae).filter(Poomsae.name == name).first()

    def add(self, poomsae: Poomsae) -> None:
        self.session.add(poomsae)

    def remove(self, uuid: UUID) -> Optional[Poomsae]:
        return self.session.query(Poomsae).filter(Poomsae.id == uuid).delete()

    def update(self, poomsae: Poomsae) -> None:
        self.session.query(Poomsae).filter(Poomsae.id == poomsae.id).update(poomsae)

    def iter(self) -> Iterator[Poomsae]:
        return self.session.query(Poomsae).all()
