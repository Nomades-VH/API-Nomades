from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.user.entities import User
from app.kibon_donjak.entities import KibonDonjak as KibonDonjakEntity


class KibonDonjak(BaseModel):
    name: str
    description: str
    fk_band: Optional[UUID] = None

    def to_create(self, user: User) -> KibonDonjakEntity:
        return KibonDonjakEntity(
            name=self.name,
            description=self.description,
            fk_band=self.fk_band,
            created_for=user.id,
            updated_for=user.id
        )
