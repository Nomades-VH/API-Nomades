from typing import Iterator, Optional
from uuid import UUID
from app.band.entities import Band as BandEntity
from app.band.models import Band as BandModel
from app.user.models import User
from ports.uow import AbstractUow


def get(uow: AbstractUow) -> Iterator[BandEntity]:
    with uow:
        yield from uow.band.iter()


def get_by_user(uow: AbstractUow, user: User) -> BandEntity:
    with uow:
        return uow.band.get(user.fk_band)


def get_by_id(uow: AbstractUow, id: UUID) -> Optional[BandEntity]:
    with uow:
        return uow.band.get(id)


def get_by_gub(uow: AbstractUow, gub: int) -> Optional[BandEntity]:
    with uow:
        return uow.band.get_by_gub(gub)


def get_by_name(uow: AbstractUow, name: str) -> Optional[BandEntity]:
    with uow:
        return uow.band.get_by_name(name)


def add(uow: AbstractUow, band: BandEntity) -> None:
    with uow:
        uow.band.add(band)


def update(uow: AbstractUow, band: BandEntity) -> None:
    with uow:
        uow.band.update(band)


def delete(uow: AbstractUow, uuid: UUID):
    with uow:
        uow.band.remove(uuid)


def to_entity(band_entity: BandEntity, band_model: BandModel) -> BandEntity:
    band_entity.gub = band_model.gub
    band_entity.name = band_model.name
    band_entity.meaning = band_model.meaning
    band_entity.fk_theory = band_model.fk_theory
    return band_entity


def to_model(band_entity: BandEntity) -> BandModel:
    return BandModel(
        gub=band_entity.gub,
        name=band_entity.name,
        meaning=band_entity.meaning,
        fk_theory=band_entity.fk_theory
    )


def to_model_dict(band_dict: dict) -> BandModel:
    return BandModel(
        gub=band_dict['gub'],
        name=band_dict['name'],
        meaning=band_dict['meaning'],
        fk_theory=band_dict['fk_theory']
    )
