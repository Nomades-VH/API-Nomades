from typing import Iterator

from app.poomsae.entities import Poomsae as PoomsaeEntity
from app.poomsae.models import Poomsae as PoomsaeModel
from ports.uow import AbstractUow


# TODO: Create a service get_all poomsae
def get_all_poomsaes(uow: AbstractUow) -> Iterator[PoomsaeEntity]:
    with uow:
        yield from uow.poomsae.iter()


def add(uow: AbstractUow, poomsae: PoomsaeEntity):
    with uow:
        uow.poomsae.add(poomsae)


# TODO: Create a service get poomsae
def get_poomsae():
    ...


# TODO: Create a service post poomsae
def post_poomsae():
    pass


# TODO: Create a service put poomsae
def put_poomsae():
    pass


# TODO: Create a service delete poomsae
def delete_poomsae():
    pass
