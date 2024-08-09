from dataclasses import dataclass, field
from typing import Optional, List
from uuid import UUID

from app.kibon_donjak.entities import KibonDonjak
from app.kick.entities import Kick
from app.poomsae.entities import Poomsae
from ports.entity import Entity


@dataclass
class Band(Entity):
    gub: int
    name: str
    meaning: str
    theory: str
    breakdown: str
    stretching: str
    updated_for: UUID
    created_for: Optional[UUID] = None
    kicks: Optional[List[Kick]] = field(default_factory=list)
    poomsaes: Optional[List[Poomsae]] = field(default_factory=list)
    kibon_donjaks: Optional[List[KibonDonjak]] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> "Band":
        return cls(
            *data
        )

    def __eq__(self, other):
        verify_poomsaes = True
        verify_kibon_donjaks = True
        verify_kicks = True

        for poomsae in self.poomsaes:
            if poomsae.id not in other.poomsaes:
                verify_poomsaes = False

        for kick in self.kicks:
            if kick.id not in other.kicks:
                verify_kicks = False

        for kibon_donjak in self.kibon_donjaks:
            if kibon_donjak.id not in other.kibon_donjaks:
                verify_kibon_donjaks = False


        return (
            self.gub == other.gub
            and self.name == other.name
            and self.meaning == other.meaning
            and self.theory == other.theory
            and self.breakdown == other.breakdown
            and self.stretching == other.stretching
            and verify_kicks
            and verify_kibon_donjaks
            and verify_poomsaes
        )
