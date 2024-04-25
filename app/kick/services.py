from typing import List, Optional
from uuid import UUID

from app.kick.entities import Kick as KickEntity
from app.kick.models import Kick as KickModel
from ports.uow import AbstractUow


def get(uow: AbstractUow) -> Optional[List[KickEntity]]:
    with uow:
        return uow.kick.iter()


def get_by_id(uow: AbstractUow, uuid: UUID) -> Optional[KickEntity]:
    with uow:
        return uow.kick.get(uuid)


# TODO: Create a service for post kick
def add(uow: AbstractUow, kick: KickEntity):
    with uow:
        uow.kick.add(kick)


def get_by_name(uow: AbstractUow, name: str):
    with uow:
        return uow.kick.get_by_name(name)


# TODO: Create a service for put kick
def update(uow: AbstractUow, kick: KickEntity) -> None:
    with uow:
        return uow.kick.update(kick)


# TODO: Create a service for delete kick
def delete(uow: AbstractUow, uuid: UUID) -> None:
    with uow:
        return uow.kick.remove(uuid)


def to_update(kick_entity: KickEntity, kick_model: KickModel) -> KickEntity:
    kick_entity.name = kick_model.name
    kick_entity.description = kick_model.description
    return kick_entity
