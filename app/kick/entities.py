from dataclasses import dataclass
from uuid import UUID

from general_enum.difficulty import Difficulty
from ports.entity import Entity


@dataclass
class Kick(Entity):
    name: str
    description: str
    difficulty: Difficulty
    fk_band: UUID
    # TODO: Adicionar "created_for" e "updated_for"
