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
