from dataclasses import dataclass

from general_enum.difficulty import Difficulty
from ports.entity import Entity


@dataclass
class KibonDonjak(Entity):
    name: str
    description: str
    difficulty: Difficulty
