from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from app.band.entities import Band as BandEntity
from app.user.entities import User
from app.kick.services import get_by_id as get_kick_by_id
from app.poomsae.services import get_by_id as get_poomsae_by_id
from app.kibon_donjak.services import get_by_id as get_kibon_donjak_by_id
from ports.uow import AbstractUow


class Band(BaseModel):
    gub: int
    name: str
    meaning: str
    theory: str
    breakdown: str
    stretching: str
    kicks: Optional[List[UUID]] = []
    poomsaes: Optional[List[UUID]] = []
    kibon_donjaks: Optional[List[UUID]] = []

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

    def __eq__(self, other):
        return self.gub == other.gub and self.name == other.name and self.meaning == other.meaning and self.theory == other.theory \
            and self.breakdown == other.breakdown and self.stretching == other.stretching
