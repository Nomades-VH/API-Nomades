from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.user.entities import User
from general_enum.difficulty import Difficulty
from app.kibon_donjak.entities import KibonDonjak as KibonDonjakEntity


class KibonDonjak(BaseModel):
    name: str
    description: str
    difficulty: Difficulty
    fk_band: Optional[UUID] = None

    def to_create(self, user: User) -> KibonDonjakEntity:
        return KibonDonjakEntity(
            name=self.name,
            description=self.description,
            difficulty=self.difficulty,
            fk_band=self.fk_band,
            created_for=user.id,
            updated_for=user.id
        )
