from typing import Optional, List

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from app.kibon_donjak.entities import KibonDonjak
from app.kick.entities import Kick
from app.poomsae.entities import Poomsae
from ports.entity import Entity


class Band(Entity):
    __tablename__ = 'bands'  # Nome da tabela
    gub: Mapped[int] = Column(Integer, unique=True, nullable=False)
    name: Mapped[str] = Column(String(50), unique=True, nullable=False)
    meaning: Mapped[str] = Column(String(600), nullable=False)
    theory: Mapped[str] = Column(String(600), nullable=False)
    breakdown: Mapped[str] = Column(String(600), nullable=False)
    stretching: Mapped[str] = Column(String(600), nullable=False)

    users = relationship("User", back_populates='band')
    kibon_donjaks: Mapped[Optional[List[KibonDonjak]]] = relationship(
        secondary="band_kibon_donjak",
        back_populates="bands",
        lazy="joined"
    )

    kicks: Mapped[Optional[List[Kick]]] = relationship(
        secondary="band_kick",
        back_populates="bands",
        lazy="joined"
    )

    poomsaes: Mapped[Optional[List[Poomsae]]] = relationship(
        secondary="band_poomsae",
        back_populates="bands",
        lazy="joined"
    )

    def __eq__(self, other):
        def verify_entities_list(first_list, second_list):
            return len(first_list) == len(second_list) and first_list == second_list

        if not verify_entities_list(self.poomsaes, other.poomsaes):
            return False

        if not verify_entities_list(self.kibon_donjaks, other.kibon_donjaks):
            return False

        if not verify_entities_list(self.kicks, other.kicks):
            return False

        return (
            self.gub == other.gub
            and self.name == other.name
            and self.meaning == other.meaning
            and self.theory == other.theory
            and self.breakdown == other.breakdown
            and self.stretching == other.stretching
        )
