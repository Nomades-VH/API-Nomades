from abc import ABC
from typing import Iterator, Optional
from uuid import UUID

from app.breakdown.entities import Breakdown, BandBreakdown
from ports.repository import AbstractRepository


class AbstractBreakdownRepository(AbstractRepository[Breakdown], ABC):
    pass


class AbstractBandBreakdownRepository(AbstractRepository[BandBreakdown], ABC):

    def get_band_breakdown(self, band_breakdown: BandBreakdown) -> Optional[BandBreakdown]:
        pass

    def remove_band_breakdown(self, band_breakdown: BandBreakdown) -> None:
        pass


class BreakdownRepository(AbstractBreakdownRepository):

    def get(self, id: UUID) -> Optional[Breakdown]:
        return self.session.query(Breakdown).filter(Breakdown.id == id).first()

    def add(self, breakdown: Breakdown) -> None:
        self.session.add(breakdown)

    def remove(self, uuid: UUID) -> Optional[Breakdown]:
        return self.session.query(Breakdown).filter(Breakdown.id == uuid).delete()

    def update(self, breakdown: dict) -> None:
        self.session.query(Breakdown).filter(Breakdown.id == breakdown["id"]).update(breakdown)

    def iter(self) -> Iterator[Breakdown]:
        return self.session.query(Breakdown).all()


class BandBreakdownRepository(AbstractBandBreakdownRepository):

    def get(self, id: UUID) -> Optional[BandBreakdown]:
        pass

    def add(self, band_breakdown: BandBreakdown) -> None:
        self.session.add(band_breakdown)

    def remove(self, band_breakdown: BandBreakdown) -> None:
        pass

    def update(self, band_breakdown: BandBreakdown) -> None:
        pass

    def iter(self) -> Iterator[BandBreakdown]:
        pass

    def get_band_breakdown(self, band_breakdown: BandBreakdown) -> Optional[BandBreakdown]:
        return self.session.query(BandBreakdown).filter(
                BandBreakdown.fk_band == band_breakdown.fk_band and
                BandBreakdown.fk_breakdown == band_breakdown.fk_breakdown
            ).first()

    def remove_band_breakdown(self, band_breakdown: BandBreakdown) -> None:
        self.session.query(BandBreakdown).filter(
                BandBreakdown.fk_band == band_breakdown.fk_band and
                BandBreakdown.fk_breakdown == band_breakdown.fk_breakdown
            ).delete()
