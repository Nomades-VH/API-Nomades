from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import relationship

from general_enum.difficulty import Difficulty
from ports.entity import Entity


@dataclass
class Poomsae(Entity):
    name: str
    description: str
    difficulty: Difficulty
    updated_for: UUID
    fk_band: UUID
    created_for: Optional[UUID] = None

