from typing import Optional

from pydantic import BaseModel, EmailStr


class Credentials(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: str
    confirmPassword: str = None
