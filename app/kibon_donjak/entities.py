from dataclasses import dataclass
from uuid import UUID

from general_enum.difficulty import Difficulty
from ports.entity import Entity


@dataclass
class KibonDonjak(Entity):
    name: str
    description: str
    difficulty: Difficulty
    created_for: UUID
    updated_for: UUID
