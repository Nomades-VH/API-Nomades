from uuid import UUID

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str
    password: str
    fk_band: UUID
