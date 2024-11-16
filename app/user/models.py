from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.auth.schemas import Credentials
from general_enum.hubs import Hubs
from general_enum.permissions import Permissions


class User(BaseModel):
    credentials: Credentials
    permission: Permissions
    src_profile: str = None
    hub: Hubs
    fk_band: Optional[UUID] = None
