from dataclasses import dataclass
from typing import Optional
from uuid import UUID
from ports.entity import Entity


@dataclass
class KibonDonjak(Entity):
    name: str
    description: str
    fk_band: UUID
    updated_for: UUID
    created_for: Optional[UUID]
