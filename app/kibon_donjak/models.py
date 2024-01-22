from pydantic import BaseModel

from app.user.entities import User
from general_enum.difficulty import Difficulty
from app.kibon_donjak.entities import KibonDonjak as KibonDonjakEntity


class KibonDonjak(BaseModel):
    name: str
    description: str
    difficulty: Difficulty

    def to_create(self, user: User) -> KibonDonjakEntity:
        return KibonDonjakEntity(
            name=self.name,
            description=self.description,
            difficulty=self.difficulty,
            created_for=user.id,
            updated_for=user.id
        )
