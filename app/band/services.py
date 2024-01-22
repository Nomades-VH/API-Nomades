from dataclasses import asdict
from typing import Optional, Any
from uuid import UUID
from app.band.entities import Band as BandEntity
from app.band.models import Band as BandModel
from app.user.models import User
from ports.uow import AbstractUow


def get(uow: AbstractUow) -> list[Optional[Any]]:
    with uow:
        return list(map(asdict, uow.band.iter()))


def get_by_user(uow: AbstractUow, user: User) -> BandEntity:
    with uow:
        return uow.band.get(user.fk_band)


def get_by_id(uow: AbstractUow, uuid: UUID) -> Optional[BandEntity]:
    with uow:
        return uow.band.get(uuid)


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


def to_update(band_entity: BandEntity, band_model: BandModel, updated_for) -> BandEntity:
    band_entity.gub = band_model.gub
    band_entity.name = band_model.name
    band_entity.meaning = band_model.meaning
    band_entity.theory = band_model.theory
    band_entity.breakdown = band_model.breakdown
    band_entity.stretching = band_model.stretching
    band_entity.updated_for = updated_for
    return band_entity


def to_model(band_entity: BandEntity) -> BandModel:
    return BandModel(
        gub=band_entity.gub,
        name=band_entity.name,
        meaning=band_entity.meaning,
        theory=band_entity.theory,
        breakdown=band_entity.breakdown,
        stretching=band_entity.stretching
    )


def to_model_dict(band_dict: dict) -> BandModel:
    return BandModel(
        gub=band_dict['gub'],
        name=band_dict['name'],
        meaning=band_dict['meaning'],
        fk_theory=band_dict['fk_theory']
    )
