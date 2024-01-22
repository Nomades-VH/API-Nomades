from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from general_enum.difficulty import Difficulty
from ports.entity import Entity


@dataclass
class Poomsae(Entity):
    name: str
    description: str
    difficulty: Difficulty
    updated_for: UUID
    fk_band: Optional[UUID] = None
    created_for: Optional[UUID] = None

