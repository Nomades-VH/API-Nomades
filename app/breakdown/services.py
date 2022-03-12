import uuid
from typing import Iterator, Optional
from uuid import UUID

from app.breakdown.entities import Breakdown, BandBreakdown
from app.breakdown.models import Breakdown as BreakdownModel
from ports.uow import AbstractUow


def get_all_breakdowns(uow: AbstractUow) -> Optional[Iterator[Breakdown]]:
    with uow:
        return uow.breakdown.iter()


def get_breakdown_by_id(breakdown_id: UUID, uow: AbstractUow) -> Optional[BreakdownModel]:
    with uow:
        breakdown = uow.breakdown.get(breakdown_id)
        return make_model_breakdown(breakdown)


def add_breakdown(model: BreakdownModel, uow: AbstractUow) -> UUID:
    with uow:
        breakdown = make_breakdown(model)
        uow.breakdown.add(breakdown)

        return breakdown.id


def add_band_breakdown(band_id: UUID, breakdown_id: UUID, uow: AbstractUow) -> None:
    with uow:
        band_breakdown = make_band_breakdown(band_id, breakdown_id)
        uow.breakdown.add_band_breakdown(band_breakdown)


def make_breakdown(model: BreakdownModel) -> Breakdown:
    return Breakdown(
        id=uuid.uuid4(),
        name=model.name,
        description=model.description,
    )


def make_model_breakdown(breakdown: Breakdown) -> BreakdownModel:
    return BreakdownModel(
        name=breakdown.name,
        description=breakdown.description,
    )


def make_band_breakdown(band_id: UUID, breakdown_id: UUID) -> BandBreakdown:
    return BandBreakdown(
        fk_band=band_id,
        fk_breakdown=breakdown_id,
    )
