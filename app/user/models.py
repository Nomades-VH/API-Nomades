from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.auth.schemas import Credentials
from general_enum.permissions import Permissions


class User(BaseModel):
    username: str
    credentials: Credentials
    permission: Permissions
    fk_band: Optional[UUID] = None
