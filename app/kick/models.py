from pydantic import BaseModel

from app.user.entities import User
from general_enum.difficulty import Difficulty
from app.kick.entities import Kick as KickEntity


# TODO: Create a model for the kick
class Kick(BaseModel):
    name: str
    description: str
    difficulty: Difficulty

    def to_create(self, user: User):
        return KickEntity(
            name=self.name,
            description=self.description,
            difficulty=self.difficulty
        )

