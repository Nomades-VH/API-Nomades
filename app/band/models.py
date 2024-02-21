from typing import Optional, List

from pydantic import BaseModel
from app.band.entities import Band as BandEntity
from app.kibon_donjak.models import KibonDonjak
from app.kick.entities import Kick
from app.poomsae.entities import Poomsae
from app.user.entities import User


class Band(BaseModel):
    gub: int
    name: str
    meaning: str
    theory: str
    breakdown: str
    stretching: str
    kicks: Optional[List[Kick]] = None
    poomsaes: Optional[List[Poomsae]] = None
    kibon_donjaks: Optional[List[KibonDonjak]] = None

    def to_create(self, user: User) -> BandEntity:
        return BandEntity(
            gub=self.gub,
            name=self.name,
            meaning=self.meaning,
            theory=self.theory,
            breakdown=self.breakdown,
            stretching=self.stretching,
            created_for=user.id,
            updated_for=user.id
        )
