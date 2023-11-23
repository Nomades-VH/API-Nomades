from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Band(BaseModel):
    gub: int
    name: str
    meaning: str
    fk_theory: UUID
