# TODO: Create a service for get_all kicks
from app.kick.entities import Kick as KickEntity
from ports.uow import AbstractUow


def get_all_kicks():
    pass


# TODO: Create a service for get kick
def get_kick():
    pass


# TODO: Create a service for post kick
def add(uow: AbstractUow, kick: KickEntity):
    with uow:
        uow.kick.add(kick)


def get_by_name(uow: AbstractUow, name: str):
    with uow:
        return uow.kick.get_by_name(name)



# TODO: Create a service for put kick
def put_kick():
    pass


# TODO: Create a service for delete kick
def delete_kick():
    pass
