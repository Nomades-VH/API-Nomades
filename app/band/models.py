from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class Band(BaseModel):
    gub: int
    name: str
    meaning: str
    created_for: str
    updated_for: Optional[str]
    fk_theory: UUID
