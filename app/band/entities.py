from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from ports.entity import Entity


@dataclass
class Band(Entity):
    gub: int
    name: str
    meaning: str
    created_for: str
    updated_for: Optional[str]
    fk_theory: Optional[UUID] = None
