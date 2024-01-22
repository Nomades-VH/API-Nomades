from dataclasses import dataclass
from typing import Optional
from uuid import UUID

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

    @classmethod
    def from_dict(cls, data: dict, user: User) -> "Band":
        return cls(
            **data,
            created_for=user.id,
            updated_for=user.id
        )
