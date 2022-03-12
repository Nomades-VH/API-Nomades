from pydantic import BaseModel


class Breakdown(BaseModel):
    name: str
    description: str
