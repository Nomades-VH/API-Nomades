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
        def verify_list_equality(self_list, list_ids):
            self_list_ids = {item.id for item in self_list}
            return len(self_list) == len(list_ids) and self_list_ids == set(list_ids)

        if not verify_list_equality(self.poomsaes, other.poomsaes):
            return False

        if not verify_list_equality(self.kibon_donjaks, other.kibon_donjaks):
            return False

        if not verify_list_equality(self.kicks, other.kicks):
            return False

        return (
            self.gub == other.gub
            and self.name == other.name
            and self.meaning == other.meaning
            and self.theory == other.theory
            and self.breakdown == other.breakdown
            and self.stretching == other.stretching
        )
