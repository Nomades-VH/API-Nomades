from typing import Iterator
from uuid import UUID

from app.poomsae.entities import Poomsae as PoomsaeEntity
from app.poomsae.models import Poomsae as PoomsaeModel
from ports.uow import AbstractUow


def get(uow: AbstractUow) -> Iterator[PoomsaeEntity]:
    with uow:
        yield from uow.poomsae.iter()


def add(uow: AbstractUow, poomsae: PoomsaeEntity):
    with uow:
        uow.poomsae.add(poomsae)


def get_by_name(uow: AbstractUow, name: str) -> PoomsaeEntity:
    with uow:
        return uow.poomsae.get_by_name(name=name)


def get_by_id(uow: AbstractUow, id: UUID) -> PoomsaeEntity:
    with uow:
        return uow.poomsae.get(id)


def update(uow: AbstractUow, poomsae: PoomsaeEntity):
    with uow:
        uow.poomsae.update(poomsae)


def delete(uow: AbstractUow, uuid: UUID) -> None:
    with uow:
        uow.poomsae.remove(uuid)


def to_update(entity: PoomsaeEntity, model: PoomsaeModel, updated_for: UUID):
    entity.name = model.name
    entity.description = model.description
    entity.difficulty = model.difficulty
    entity.updated_for = updated_for
    return entity