from dataclasses import dataclass

from ports.entity import Entity


@dataclass
class Theory(Entity):
    description: str
