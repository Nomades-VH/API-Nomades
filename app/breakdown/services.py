import uuid
from dataclasses import asdict
from datetime import datetime
from typing import Iterator, Optional
from uuid import UUID

from app.breakdown.entities import Breakdown, BandBreakdown
from app.breakdown.models import Breakdown as BreakdownModel
from ports.uow import AbstractUow


# TODO: Revisar todos os serviços
def get_all(uow: AbstractUow) -> Optional[Iterator[Breakdown]]:
    with uow:
        return uow.breakdown.iter()


def get_by_id(breakdown_id: UUID, uow: AbstractUow) -> Optional[Breakdown]:
    with uow:
        return uow.breakdown.get(breakdown_id)


def add(model: BreakdownModel, uow: AbstractUow) -> UUID:
    with uow:
        breakdown = make_breakdown(model)
        uow.breakdown.add(breakdown)

        return breakdown.id


def update(
    breakdown_id: UUID, model_new: BreakdownModel, uow: AbstractUow
) -> None:
    with uow:
        breakdown = get_by_id(breakdown_id, uow)
        if breakdown is not None:
            created_at = breakdown.created_at
            breakdown_new = make_breakdown_update(breakdown_id, model_new, created_at)
            uow.breakdown.update(breakdown_new)
        return


def add_band_breakdown(band_id: UUID, breakdown_id: UUID, uow: AbstractUow) -> None:
    with uow:
        band_breakdown = make_band_breakdown(band_id, breakdown_id)
        uow.band_breakdown.add(band_breakdown)


def make_breakdown(model: BreakdownModel) -> Breakdown:
    return Breakdown(
        id=uuid.uuid4(),
        name=model.name,
        description=model.description,
    )


def make_breakdown_update(
    id: UUID, model_breakdown_new: BreakdownModel, created_at: datetime
) -> Breakdown:
    breakdown_new = Breakdown(
            id=id,
            name=model_breakdown_new.name,
            description=model_breakdown_new.description,
        )
    breakdown_new.updated_at=datetime.now()
    breakdown_new.created_at=created_at
    return breakdown_new


def make_band_breakdown(band_id: UUID, breakdown_id: UUID) -> BandBreakdown:
    return BandBreakdown(
        fk_band=band_id,
        fk_breakdown=breakdown_id,
    )


def remove_breakdown(band_id: UUID, breakdown_id: UUID, uow: AbstractUow) -> None:
    with uow:
        breakdown = get_by_id(breakdown_id, uow)
        if breakdown is not None:
            remove_band_breakdown(band_id, breakdown_id, uow)
            uow.breakdown.remove(breakdown.id)


def remove_band_breakdown(band_id: UUID, breakdown_id: UUID, uow: AbstractUow) -> None:
    with uow:
        band_breakdown = make_band_breakdown(band_id, breakdown_id)
        band_breakdown = uow.band_breakdown.get_band_breakdown(band_breakdown)
        if band_breakdown is not None:
            uow.band_breakdown.remove_band_breakdown(band_breakdown)
