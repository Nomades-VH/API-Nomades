import dataclasses
from abc import ABC
from typing import Optional, Iterator
from uuid import UUID
from app.band.entities import Band
from ports.repository import AbstractRepository


class AbstractBandRepository(AbstractRepository[Band], ABC):
    def get_by_gub(self, gub: int) -> Optional[Band]:
        pass

    def get_by_name(self, name: str) -> Optional[Band]:
        pass

    def remove_by_name(self, name: str) -> Optional[Band]:
        pass


class BandRepository(AbstractBandRepository):
    def get(self, id: UUID) -> Optional[Band]:
        return self.session.query(Band).filter(Band.id == id).first()

    def get_by_gub(self, gub: int) -> Optional[Band]:
        return self.session.query(Band).filter(Band.gub == gub).first()

    def get_by_name(self, name: str) -> Optional[Band]:
        return self.session.query(Band).filter(Band.name == name).first()

    def add(self, band: Band) -> None:
        self.session.add(band)

    def remove(self, uuid: UUID) -> Optional[Band]:
        return self.session.query(Band).filter(Band.id == uuid).delete()

    def update(self, band: Band) -> None:
        self.session.query(Band).filter(Band.id == band.id).update(dataclasses.asdict(band))

    def iter(self) -> Iterator[Band]:
        yield from self.session.query(Band).all()

    # TODO: Create a method to remove band with name
    def remove_by_name(self, name: str) -> Optional[Band]:
        pass
