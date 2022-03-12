from dataclasses import dataclass
from uuid import UUID

from ports.entity import Entity


@dataclass
class Breakdown(Entity):
    id: UUID
    name: str
    description: str


@dataclass
class BandBreakdown(Entity):
    fk_band: UUID
    fk_breakdown: UUID
