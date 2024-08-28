# TODO: Create a service for get_all KibonDonjaks
from dataclasses import asdict
from typing import List, Optional
from uuid import UUID

from app.kibon_donjak.entities import KibonDonjak as KibonDonjakEntity
from app.kibon_donjak.models import KibonDonjak as KibonDonjakModel
from ports.uow import AbstractUow


def get(uow: AbstractUow):
    with uow:
        return list(map(asdict, uow.kibondonjak.iter()))


def get_by_band(uow: AbstractUow, uuid: UUID) -> Optional[List[KibonDonjakEntity]]:
    with uow:
        band = uow.band.get(uuid)
        if band:
            return band.kibon_donjaks


def get_by_name(uow: AbstractUow, name):
    with uow:
        return uow.kibondonjak.get_by_name(name)


# TODO: Create a service for the post KiBonDonjak
def add(uow: AbstractUow, kibondonjak: KibonDonjakEntity):
    with uow:
        uow.kibondonjak.add(kibondonjak)


# TODO: Create a service for the put KiBonDonjak
def update(uow: AbstractUow, kibon_donjak: KibonDonjakEntity):
    with uow:
        return uow.kibondonjak.update(kibon_donjak)


def to_update(
    entity: KibonDonjakEntity, model: KibonDonjakModel, uow: AbstractUow = None
) -> KibonDonjakEntity:
    entity.name = model.name
    entity.description = model.description
    return entity


# TODO: Create a service for the delete KiBonDonjak
def delete(uow: AbstractUow, uuid: UUID):
    with uow:
        return uow.kibondonjak.remove(uuid)


def get_by_id(uow: AbstractUow, uuid: UUID) -> Optional[KibonDonjakEntity]:
    with uow:
        return uow.kibondonjak.get(uuid)
