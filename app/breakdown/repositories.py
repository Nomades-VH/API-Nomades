from abc import ABC
from typing import Iterator, Optional
from uuid import UUID

from app.breakdown.entities import Breakdown, BandBreakdown
from ports.repository import AbstractRepository


class AbstractBreakdownRepository(AbstractRepository[Breakdown], ABC):

    def add_band_breakdown(self, band_breakdown: BandBreakdown) -> None:
        pass


class BreakdownRepository(AbstractBreakdownRepository):

    def get(self, id: UUID) -> Optional[Breakdown]:
        return self.session.query(Breakdown).filter(Breakdown.id == id).first()

    def add(self, breakdown: Breakdown) -> UUID:
        self.session.add(breakdown)

    def remove(self, uuid: UUID) -> Optional[Breakdown]:
        return self.session.query(Breakdown).filter(Breakdown.id == uuid).delete()

    def update(self, breakdown: Breakdown) -> None:
        self.session.query(Breakdown).filter(Breakdown.id == breakdown.id).update(breakdown)

    def add_band_breakdown(self, band_breakdown: BandBreakdown) -> None:
        self.session.add(band_breakdown)

    def iter(self) -> Iterator[Breakdown]:
        return self.session.query(Breakdown).all()
