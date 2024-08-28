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
        def verify_entities_list(first_list, second_list):
            return len(first_list) == len(second_list) and first_list == second_list

        if not verify_entities_list(self.poomsaes, other.poomsaes):
            return False

        if not verify_entities_list(self.kibon_donjaks, other.kibon_donjaks):
            return False

        if not verify_entities_list(self.kicks, other.kicks):
            return False

        return (
            self.gub == other.gub
            and self.name == other.name
            and self.meaning == other.meaning
            and self.theory == other.theory
            and self.breakdown == other.breakdown
            and self.stretching == other.stretching
        )
