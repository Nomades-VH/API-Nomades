from uuid import UUID

from pydantic import BaseModel

from general_enum.difficulty import Difficulty


# TODO: Create a model for the poomsae if necessary
class Poomsae(BaseModel):
    name: str
    description: str
    difficulty: Difficulty
    fk_band: UUID
