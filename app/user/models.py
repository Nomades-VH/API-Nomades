from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.auth.schemas import Credentials
from general_enum.hubs import Hubs
from general_enum.permissions import Permissions


class User(BaseModel):
    credentials: Credentials
    permission: Permissions
    hub: Hubs
    fk_band: Optional[UUID] = None
