from typing import Iterator

from app.poomsae.entities import Poomsae as PoomsaeEntity
from ports.uow import AbstractUow


# TODO: Create a service get_all poomsae
def get_all_poomsaes(uow: AbstractUow) -> Iterator[PoomsaeEntity]:
    with uow:
        yield from uow.poomsae.iter()


def add(uow: AbstractUow, poomsae):
    with uow:
        poomsae = poomsae.to_entity()
        print(type(poomsae))
        uow.poomsae.add(poomsae)


def get_by_name(uow: AbstractUow, name: str) -> PoomsaeEntity:
    with uow:
        return uow.poomsae.get_by_name(name=name)

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
