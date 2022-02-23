from dataclasses import dataclass

from ports.entity import Entity


@dataclass
class Breakdown(Entity):
    name: str
    description: str