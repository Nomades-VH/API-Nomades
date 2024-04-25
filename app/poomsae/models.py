from typing import Optional
from uuid import UUID
from pydantic import BaseModel

from app.user.entities import User
from app.poomsae.entities import Poomsae as PoomsaeEntity


class Poomsae(BaseModel):
    name: str
    description: str
    fk_band: Optional[UUID] = None

    # TODO: Isso deve ser padrão para o projeto inteiro
    #  Invés de criar um serviço para realizar isso, fazer direto no model ou entity
    def to_create(self, user: User) -> PoomsaeEntity:
        return PoomsaeEntity(
            name=self.name,
            description=self.description,
            fk_band=self.fk_band,
            created_for=user.id,
            updated_for=user.id
        )
