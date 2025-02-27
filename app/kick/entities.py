from typing import List
from uuid import UUID as PyUUID

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from ports.entity import Entity


class Kick(Entity):
    __tablename__ = 'kicks'
    name: Mapped[str] = Column(String(50), unique=True, nullable=False)
    description: Mapped[str] = Column(String(600), nullable=False)

    bands: Mapped['Band'] = relationship(
        secondary='band_kick', back_populates='kicks'
    )


class BandKick(Entity):
    __tablename__ = 'band_kick'

    band_id: PyUUID = Column(
        SQLUUID(as_uuid=True),
        ForeignKey('bands.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
    )
    kick_id: PyUUID = Column(
        SQLUUID(as_uuid=True),
        ForeignKey('kicks.id', ondelete='CASCADE'),
        primary_key=True,
        nullable=False,
    )
