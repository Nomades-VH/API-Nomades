from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID

from app.kibon_donjak.entities import KibonDonjak
from app.kick.entities import Kick
from app.poomsae.entities import Poomsae
from app.user.entities import User
from ports.entity import Entity


@dataclass
class Band(Entity):
    gub: int
    name: str
    meaning: str
    theory: str
    breakdown: str
    stretching: str
    updated_for: UUID
    created_for: Optional[UUID] = None
    kicks: List[Kick] = field(default_factory=list)
    poomsaes: List[Poomsae] = field(default_factory=list)
    kibon_donjaks: List[KibonDonjak] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict, user: User) -> "Band":
        return cls(
            **data,
            created_for=user.id,
            updated_for=user.id
        )
