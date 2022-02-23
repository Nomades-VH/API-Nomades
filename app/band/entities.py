from dataclasses import dataclass
from uuid import UUID

from ports.entity import Entity


@dataclass
class Band(Entity):
    gub: int
    name: str
    meaning: str
    fk_theory: UUID
