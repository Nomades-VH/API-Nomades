from dataclasses import dataclass

from general_enum.difficulty import Difficulty
from ports.entity import Entity

@dataclass
class Stretching(Entity):
    name: str
    description: str
    difficulty: Difficulty
