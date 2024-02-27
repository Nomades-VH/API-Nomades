from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from general_enum.difficulty import Difficulty
from ports.entity import Entity


@dataclass
class KibonDonjak(Entity):
    name: str
    description: str
    difficulty: Difficulty
    fk_band: UUID
    updated_for: UUID
    created_for: Optional[UUID]
