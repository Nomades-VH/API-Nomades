from abc import abstractmethod, ABC
from typing import List, Optional
from uuid import UUID

from app.band.entities import Band
from ports.repository import AbstractRepository


class AbstractBandRepository(AbstractRepository[Band], ABC):

    @abstractmethod
    def find_minors_gub(self, gub: int) -> List[Band]:
        pass


class BandRepository(AbstractBandRepository):

    def get(self, id: UUID) -> Optional[Band]:
        return self.session.query(Band).filter(Band.id == id).first()

    def add(self, band: Band) -> None:
        self.session.add(band)

    def remove(self, band: Band) -> None:
        self.session.query(Band).filter(Band.id == band.id).delete()

    def update(self, band: Band) -> None:
        self.session.query(Band).filter(Band.id == band.id).update(band)

    def iter(self) -> List[Band]:
        yield from self.session.query(Band).all()

    def find_minors_gub(self, gub: int) -> List[Band]:
        yield from self.session.query(Band).filter(gub > Band.gub).all()
