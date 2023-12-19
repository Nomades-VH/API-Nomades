from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from general_enum.permissions import Permissions
from ports.entity import Entity


@dataclass
class User(Entity):
    username: str
    email: str
    password: str
    permission: Permissions
    fk_band: Optional[UUID] = None

    @classmethod
    def to_dict(cls, user: "User") -> dict:
        return {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "password": user.password,
            "permission": user.permission,
            "fk_band": user.fk_band,
            "created_at": user.created_at,
            "updated_at": user.updated_at
        }


@dataclass
class Exame(Entity):
    fk_user: UUID
    fk_band: UUID
    note_poomsae: float
    note_kibondonjak: float
    note_kick: float
    note_stretching: float
    note_breakdown: float
    note_theory: float
