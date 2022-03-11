from typing import Iterator, Optional
from uuid import UUID

from app.band.entities import Band as BandEntity
from app.band.models import Band as BandModel
from ports.uow import AbstractUow


def get_all_bands(uow: AbstractUow) -> Iterator[BandEntity]:
    with uow:
        yield from uow.band.iter()


def get_band_by_id(uow: AbstractUow, id: UUID) -> Optional[BandEntity]:
    with uow:
        return uow.band.get(id)


def add_band(uow: AbstractUow, band: BandEntity) -> None:
    with uow:
        return uow.band.add(band)


def make_band(band_model: BandModel) -> BandEntity:
    return BandEntity(
        gub=band_model.gub,
        name=band_model.name,
        meaning=band_model.meaning,
        fk_theory=band_model.fk_theory,
    )
