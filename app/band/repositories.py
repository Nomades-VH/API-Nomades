import dataclasses
from abc import ABC
from typing import Optional, Iterator, List
from uuid import UUID

from sqlalchemy.orm import joinedload

from app.band.entities import Band
from app.kibon_donjak.entities import KibonDonjak
from app.kick.entities import Kick
from app.poomsae.entities import Poomsae
from ports.repository import AbstractRepository


class AbstractBandRepository(AbstractRepository[Band], ABC):
    def get_by_gub(self, gub: int) -> Optional[Band]:
        pass

    def get_by_name(self, name: str) -> Optional[Band]:
        pass

    def remove_by_name(self, name: str) -> Optional[Band]:
        pass


class BandRepository(AbstractBandRepository):
    def get(self, id: UUID):
        return self.session.query(Band).filter(Band.id == id).first()

    def get_by_gub(self, gub: int) -> Optional[Band]:
        return self.session.query(Band).filter(Band.gub == gub).first()

    def get_by_name(self, name: str) -> Optional[Band]:
        return self.session.query(Band).filter(Band.name == name).first()

    def add(self, band: Band) -> None:
        self.session.add(band)

    def remove(self, uuid: UUID) -> Optional[Band]:
        return self.session.query(Band).filter(Band.id == uuid).delete()

    def update(self, band: dict) -> None:
        self.session.query(Band).filter(Band.id == band['id']).update(band)

    def iter(self) -> List[Band]:
        return self.session.query(Band).all()

    # TODO: Create a method to remove band with name
    def remove_by_name(self, name: str) -> Optional[Band]:
        pass
