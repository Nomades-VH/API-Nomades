from dataclasses import dataclass
from uuid import UUID

from ports.entity import Entity


@dataclass
class Auth(Entity):
    access_token: str
    fk_user: UUID
    is_invalid: bool = False
