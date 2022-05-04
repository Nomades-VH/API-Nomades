from pydantic import BaseModel, EmailStr


class Credentials(BaseModel):
    username: EmailStr
    password: str
