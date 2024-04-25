from dataclasses import dataclass
from uuid import UUID

from ports.entity import Entity


@dataclass
class Kick(Entity):
    name: str
    description: str
    # TODO: Adicionar "created_for" e "updated_for"
