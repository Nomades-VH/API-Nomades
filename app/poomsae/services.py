from typing import Iterator
from uuid import UUID

from app.poomsae.entities import Poomsae as PoomsaeEntity
from app.poomsae.models import Poomsae as PoomsaeModel
from ports.uow import AbstractUow


# TODO: Create a service get_all poomsae
def get(uow: AbstractUow) -> Iterator[PoomsaeEntity]:
    with uow:
        yield from uow.poomsae.iter()


def add(uow: AbstractUow, poomsae):
    with uow:
        uow.poomsae.add(poomsae)


def get_by_name(uow: AbstractUow, name: str) -> PoomsaeEntity:
    with uow:
        return uow.poomsae.get_by_name(name=name)


def get_by_id(uow: AbstractUow, id: UUID) -> PoomsaeEntity:
    with uow:
        return uow.poomsae.get(id)

# TODO: Create a service get poomsae
def get_poomsae():
    ...


# TODO: Create a service post poomsae
def post_poomsae():
    pass


# TODO: Create a service put poomsae
def update(uow: AbstractUow, poomsae: PoomsaeEntity):
    with uow:
        uow.poomsae.update(poomsae)


# TODO: Create a service delete poomsae
def delete_poomsae():
    pass


def to_entity(entity: PoomsaeEntity, model: PoomsaeModel):
    entity.name = model.name
    entity.description = model.description
    entity.difficulty = model.difficulty
    return entity