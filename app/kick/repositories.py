from abc import ABC
from typing import Iterator, Optional
from uuid import UUID

from app.kick.entities import Kick
from ports.repository import AbstractRepository


class AbstractKickRepository(AbstractRepository[Kick], ABC):
    pass


class KickRepository(AbstractKickRepository):

    def get(self, uuid: UUID) -> Optional[Kick]:
        return self.session.query(Kick).filter(Kick.id == uuid).first()

    def add(self, kick: Kick) -> None:
        self.session.add(kick)

    def remove(self, uuid: UUID) -> Optional[Kick]:
        return self.session.query(Kick).filter(Kick.id == uuid).delete()

    def update(self, kick: Kick) -> None:
        self.session.query(Kick).filter(Kick.id == kick.id).update(kick)

    def iter(self) -> Iterator[Kick]:
        return self.session.query(Kick).all()
