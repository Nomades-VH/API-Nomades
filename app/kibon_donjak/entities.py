from typing import List
from uuid import UUID as PyUUID

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.orm import Mapped, relationship

from ports.entity import Entity


class KibonDonjak(Entity):
    __tablename__ = 'kibon_donjaks'
    name: Mapped[str] = Column(String(150), unique=True, nullable=False)
    description: Mapped[str] = Column(String(600), nullable=False)

    bands: Mapped['Band'] = relationship(
        secondary='band_kibon_donjak', back_populates='kibon_donjaks'
    )


class BandKibonDonjak(Entity):
    __tablename__ = 'band_kibon_donjak'

    band_id: PyUUID = Column(
        SQLUUID(as_uuid=True),
        ForeignKey('bands.id', ondelete='CASCADE'),
        primary_key=True,
    )
    kibon_donjak_id: PyUUID = Column(
        SQLUUID(as_uuid=True),
        ForeignKey('kibon_donjaks.id', ondelete='CASCADE'),
        primary_key=True,
    )
