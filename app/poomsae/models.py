from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.poomsae.entities import Poomsae as PoomsaeEntity
from app.user.entities import User


class Poomsae(BaseModel):
    name: str
    description: str

    def to_create(self, user: User, uow=None) -> PoomsaeEntity:
        return PoomsaeEntity(
            name=self.name,
            description=self.description,
            created_for=user.id,
            updated_for=user.id,
        )
