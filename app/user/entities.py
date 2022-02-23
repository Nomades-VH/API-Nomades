from dataclasses import dataclass
from uuid import UUID

from ports.entity import Entity


@dataclass
class User(Entity):
    name: str
    login: str
    password: str
    fk_band: UUID
