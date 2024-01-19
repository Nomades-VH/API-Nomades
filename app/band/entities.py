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
    created_for: str
    updated_for: Optional[str]
    fk_theory: Optional[UUID] = None

    @classmethod
    def from_dict(cls, data: dict, user: User) -> "Band":
        return cls(
            **data,
            created_for=user.username,
            updated_for=user.username
        )
