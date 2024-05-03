from dataclasses import dataclass, field
from typing import Optional
from uuid import UUID

from ports.entity import Entity


@dataclass
class Kick(Entity):
    name: str
    description: str
    created_for: UUID
    updated_for: UUID
