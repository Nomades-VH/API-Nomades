from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from app.band.entities import Band as BandEntity
from app.user.entities import User


class Band(BaseModel):
    gub: int
    name: str
    meaning: str
    fk_theory: Optional[UUID] = None

    def to_entity(self, user: User) -> BandEntity:
        return BandEntity(
            gub=self.gub,
            name=self.name,
            meaning=self.meaning,
            fk_theory=self.fk_theory,
            created_for=user.username,
            updated_for=user.username
        )
