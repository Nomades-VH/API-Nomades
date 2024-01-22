from pydantic import BaseModel
from app.band.entities import Band as BandEntity
from app.user.entities import User


class Band(BaseModel):
    gub: int
    name: str
    meaning: str
    theory: str
    breakdown: str
    stretching: str

    def to_create(self, user: User) -> BandEntity:
        return BandEntity(
            gub=self.gub,
            name=self.name,
            meaning=self.meaning,
            theory=self.theory,
            breakdown=self.breakdown,
            stretching=self.stretching,
            created_for=user.id,
            updated_for=user.id
        )

    def dict_to_model(self, data: dict) -> "Band":
        self.gub = data.get("gub")
        self.name = data.get("name")
        self.meaning = data.get("meaning")
        self.theory = data.get("theory")
        self.breakdown = data.get("breakdown")
        self.stretching = data.get("stretching")
        return self

