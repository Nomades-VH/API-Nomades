from typing import Optional
from uuid import UUID
from pydantic import BaseModel
from general_enum.difficulty import Difficulty
from app.poomsae.entities import Poomsae as PoomsaeEntity


class Poomsae(BaseModel):
    name: str
    description: str
    difficulty: Difficulty
    fk_band: Optional[UUID] = None

    # TODO: Isso deve ser padrão para o projeto inteiro
    #  Invés de criar um serviço para realizar isso, fazer direto no model ou entity
    def to_entity(self):
        return PoomsaeEntity(
            name=self.name,
            description=self.description,
            difficulty=self.difficulty,
            fk_band=self.fk_band
        )
