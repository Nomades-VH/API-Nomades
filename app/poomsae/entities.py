from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from ports.entity import Entity


@dataclass
class Poomsae(Entity):
    name: str
    description: str
    updated_for: UUID
    fk_band: UUID
    created_for: Optional[UUID] = None

