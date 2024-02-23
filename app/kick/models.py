from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.user.entities import User
from general_enum.difficulty import Difficulty
from app.kick.entities import Kick as KickEntity


# TODO: Create a model for the kick
class Kick(BaseModel):
    name: str
    description: str
    difficulty: Difficulty
    fk_band: Optional[UUID] = None

    def to_create(self, user: User) -> KickEntity:
        return KickEntity(
            name=self.name,
            description=self.description,
            difficulty=self.difficulty,
            fk_band=self.fk_band
        )

