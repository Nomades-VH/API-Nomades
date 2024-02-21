from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import relationship

from general_enum.difficulty import Difficulty
from ports.entity import Entity


@dataclass
class Kick(Entity):
    name: str
    description: str
    difficulty: Difficulty
    fk_band: UUID
