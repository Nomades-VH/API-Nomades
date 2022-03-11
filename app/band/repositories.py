from abc import ABC
from typing import Optional, Iterator
from uuid import UUID
from app.band.entities import Band
from ports.repository import AbstractRepository


class AbstractBandRepository(AbstractRepository[Band], ABC):
    pass


class BandRepository(AbstractBandRepository):

    def get(self, id: UUID) -> Optional[Band]:
        return self.session.query(Band).filter(Band.id == id).first()

    def add(self, band: Band) -> None:
        self.session.add(band)

    def remove(self, uuid: UUID) -> Optional[Band]:
        return self.session.query(Band).filter(Band.id == uuid).delete()

    def update(self, band: Band) -> None:
        self.session.query(Band).filter(Band.id == band.id).update(band)

    def iter(self) -> Iterator[Band]:
        yield from self.session.query(Band).all()
