from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from app.band.entities import Band as BandEntity
from app.uow import SqlAlchemyUow
from app.user.entities import User
from app.kick.services import get_by_id as get_kick_by_id
from app.poomsae.services import get_by_id as get_poomsae_by_id
from app.kibon_donjak.services import get_by_id as get_kibon_donjak_by_id


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

        uow = SqlAlchemyUow()
        with uow:
            kicks = []
            for id_kick in self.kicks:
                kick = get_kick_by_id(uow, id_kick)
                if kick:
                    kicks.append(kick)

            poomsaes = []
            for id_poomsae in self.poomsaes:
                poomsae = get_poomsae_by_id(uow, id_poomsae)
                if poomsae:
                    poomsaes.append(poomsae)

            kibon_donjaks = []
            for id_kibon_donjak in self.kibon_donjaks:
                kibon_donjak = get_kibon_donjak_by_id(uow, id_kibon_donjak)
                if kibon_donjak:
                    kibon_donjaks.append(kibon_donjak)

        return BandEntity(
            gub=self.gub,
            name=self.name,
            meaning=self.meaning,
            theory=self.theory,
            breakdown=self.breakdown,
            stretching=self.stretching,
            kicks=kicks,
            poomsaes=poomsaes,
            kibon_donjaks=kibon_donjaks,
            created_for=user.id,
            updated_for=user.id
        )
