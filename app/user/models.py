from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from general_enum.permissions import Permissions


class User(BaseModel):
    username: str
    email: str
    password: str
    permission: Permissions
    fk_band: Optional[UUID] = None
