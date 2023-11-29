from dataclasses import dataclass
from uuid import UUID

from app.auth.value_object import Token
from ports.entity import Entity


@dataclass
class Auth(Entity):
    access_token: str
    fk_user: UUID
    is_invalid: bool = False
