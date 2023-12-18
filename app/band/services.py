from typing import Iterator, Optional
from uuid import UUID
from app.band.entities import Band as BandEntity
from app.band.models import Band as BandModel
from app.user.models import User
from ports.uow import AbstractUow


def get_all(uow: AbstractUow) -> Iterator[BandEntity]:
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


def add(uow: AbstractUow, band: BandEntity, user: User) -> None:
    with uow:
        uow.band.add(band)


# TODO: Review a service to update
def update(uow: AbstractUow, band: BandEntity) -> None:
    with uow:
        uow.band.update(band)


# TODO: Review a service to delete
def remove(uow: AbstractUow, uuid: UUID):
    with uow:
        uow.band.remove(uuid)


def add_creator(band: BandEntity, user: User) -> BandEntity | BandModel:
    band_entity = make_band(band, user.username)
    return band_entity


def make_band(band: BandModel | BandEntity, username) -> BandEntity | BandModel:
    if type(band) == BandModel:
        return BandEntity(
            gub=band.gub,
            name=band.name,
            meaning=band.meaning,
            created_for=username,
            updated_for=username,
            fk_theory=band.fk_theory,
        )
    return BandModel(
        gub=band.gub,
        name=band.name,
        meaning=band.meaning,
        fk_theory=band.fk_theory,
    )
