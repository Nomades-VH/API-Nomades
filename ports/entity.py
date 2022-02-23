from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID


@dataclass
class Entity(ABC):
    id: UUID = field(init=False)
    created_at: datetime = field(init=False)
    updated_at: datetime = field(init=False)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False

        return self.id == other.id