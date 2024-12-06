from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.kick.entities import Kick as KickEntity
from app.user.entities import User


# TODO: Create a model for the kick
class Kick(BaseModel):
    name: str
    description: str

    def to_create(self, user: User, uow=None) -> KickEntity:
        return KickEntity(
            name=self.name,
            description=self.description,
            created_for=user.id,
            updated_for=user.id,
        )
