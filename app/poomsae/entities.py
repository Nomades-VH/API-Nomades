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
    fk_band: Optional[UUID] = None
