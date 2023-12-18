from dataclasses import dataclass
from uuid import UUID

from ports.entity import Entity


@dataclass
class Auth(Entity):
    access_token: str
    fk_user: UUID
    is_invalid: bool = False

    @classmethod
    def from_dict(cls, token_dict: dict) -> "Auth":
        return cls(
            access_token=token_dict["access_token"],
            fk_user=token_dict["fk_user"],
            is_invalid=token_dict["is_invalid"]
        )
