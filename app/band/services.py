import dataclasses
from http import HTTPStatus
from typing import Optional, List, Type
from uuid import UUID

from starlette.responses import JSONResponse

from app.band.entities import Band as BandEntity, Band
from app.band.models import Band as BandModel
from app.user.models import User
from ports.uow import AbstractUow

from app.kick.services import get_by_id as get_kick_by_id
from app.kibon_donjak.services import get_by_id as get_kibon_donjak_by_id
from app.poomsae.services import get_by_id as get_poomsae_by_id


def get(uow: AbstractUow) -> List[Optional[BandModel]]:
    with uow:
        return uow.band.iter()


def get_by_user(uow: AbstractUow, user: User) -> BandEntity:
    with uow:
        return uow.band.get(user.fk_band)


def get_by_id(uow: AbstractUow, uuid: UUID):
    with uow:
        return uow.band.get(uuid)


def get_by_gub(uow: AbstractUow, gub: int) -> Optional[BandEntity]:
    with uow:
        return uow.band.get_by_gub(gub)


def get_by_name(uow: AbstractUow, name: str) -> Optional[BandEntity]:
    with uow:
        return uow.band.get_by_name(name)


def get_minors_band(uow: AbstractUow, gub: int) -> Optional[List[BandModel]]:
    bands = uow.band.iter()
    minors: List[BandModel] = []
    for band in bands:
        if band.gub >= gub:
            minors.append(band)

    return minors


def add(uow: AbstractUow, band: BandEntity) -> None:
    with uow:
        uow.band.add(band)


def update(uow: AbstractUow, band: Band) -> None:
    with uow:
        uow.band.update(band)


def add_kicks(uuid_band: UUID, kicks: List[UUID], uow: AbstractUow):
    return add_entity(
        parent_id=uuid_band,
        entity_ids=kicks,
        uow=uow,
        entity_repo_name='kick',
        relation_attr='kicks'
    )


def add_poomsaes(
        uuid_band: UUID,
        poomsaes: List[UUID],
        uow: AbstractUow
):
    return add_entity(
        parent_id=uuid_band,
        entity_ids=poomsaes,
        uow=uow,
        entity_repo_name='poomsae',
        relation_attr='poomsaes'
    )


def add_kibon_donjaks(
        uuid_band: UUID,
        kibon_donjaks: List[UUID],
        uow: AbstractUow
):
    return add_entity(
        parent_id=uuid_band,
        entity_ids=kibon_donjaks,
        uow=uow,
        entity_repo_name='kibondonjak',
        relation_attr='kibon_donjaks'
    )


def delete_kick(uuid_band: UUID, uuid_kick: UUID, uow: AbstractUow):
    return delete_entity(parent_id=uuid_band, entity_id=uuid_kick, uow=uow, entity_repository='kick',
                         relation_attr='kicks')


def delete_poomsae(uuid_band: UUID, uuid_poomsae: UUID, uow: AbstractUow):
    return delete_entity(parent_id=uuid_band, entity_id=uuid_poomsae, uow=uow, entity_repository='poomsae',
                         relation_attr='poomsaes')


def delete_kibon_donjak(
        uuid_band: UUID,
        uuid_kibon_donjak: UUID,
        uow: AbstractUow
):
    return delete_entity(parent_id=uuid_band, entity_id=uuid_kibon_donjak, uow=uow, entity_repository='kibondonjak',
                         relation_attr='kibon_donjaks')


def add_entity(parent_id: UUID, entity_ids: List[UUID], uow: AbstractUow,
               entity_repo_name: str, relation_attr: str, parent_repo_name: str = "band"):
    with uow:
        parent = getattr(uow, parent_repo_name).get(parent_id)
        if not parent:
            return None

        for entity_id in entity_ids:
            entity = getattr(uow, entity_repo_name).get(entity_id)

            if not entity:
                uow.rollback()
                return None

            if entity not in getattr(parent, relation_attr):
                getattr(parent, relation_attr).append(entity)

    return entity_ids


def delete_entity(parent_id: UUID, entity_id: UUID, uow: AbstractUow,
                  entity_repository: str,
                  relation_attr: str,
                  parent_repository: str = 'band'
                  ) -> Optional[UUID]:
    with uow:
        parent = getattr(uow, parent_repository).get(parent_id)
        if not parent:
            return None

        entity = getattr(uow, entity_repository).get(entity_id)
        if not entity:
            return None

        # Verifica se a entidade está na lista de entidades relacionadas da entidade pai
        related_entities: List = getattr(parent, relation_attr)
        if entity not in related_entities:
            return None

        # Remove a entidade da lista de relacionamentos e persiste as alterações
        related_entities.remove(entity)

    return entity_id


def delete(uow: AbstractUow, uuid: UUID):
    with uow:
        uow.band.remove(uuid)


def to_update(band_entity: BandEntity, band_model: BandModel, uow: AbstractUow) -> BandEntity:
    band_entity.gub = band_model.gub
    band_entity.name = band_model.name
    band_entity.meaning = band_model.meaning
    band_entity.theory = band_model.theory
    band_entity.breakdown = band_model.breakdown
    band_entity.stretching = band_model.stretching

    with uow:
        for kibon_donjak in band_entity.kibon_donjaks:
            if kibon_donjak.id not in band_model.kibon_donjaks:
                delete_kibon_donjak(band_entity.id, kibon_donjak.id, uow)

        add_kibon_donjaks(band_entity.id, band_model.kibon_donjaks, uow)

        for poomsae in band_entity.poomsaes:
            if poomsae.id not in band_model.poomsaes:
                delete_poomsae(band_entity.id, poomsae.id, uow)

        add_poomsaes(band_entity.id, band_model.poomsaes, uow)

        for kick in band_entity.kicks:
            if kick.id not in band_model.kicks:
                delete_kick(band_entity.id, kick.id, uow)

        add_kicks(band_entity.id, band_model.kicks, uow)

    return band_entity
