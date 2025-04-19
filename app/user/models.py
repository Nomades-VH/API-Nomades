from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr

from app.auth.schemas import Credentials
from general_enum.hubs import Hubs
from general_enum.permissions import Permissions


class User(BaseModel):
    credentials: Credentials
    bio: str
    permission: Permissions
    src_profile: str = None
    hub: Hubs
    fk_band: Optional[UUID] = None


class BlackBands(BaseModel):
    name: str
    bio: str
    src_profile: str