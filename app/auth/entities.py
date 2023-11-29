from dataclasses import dataclass
from uuid import UUID

from ports.entity import Entity


@dataclass
class Token(Entity):
    token: str
    fk_user: UUID
