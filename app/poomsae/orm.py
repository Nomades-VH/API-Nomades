from datetime import datetime
from sqlalchemy import Enum
from uuid import uuid4

from sqlalchemy import Table, Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.band.entities import Band
from app.band.orm import band_poomsae
from app.poomsae.entities import Poomsae
from bootstrap.database import mapper_registry

poomsaes = Table(
    "poomsaes",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String[50], nullable=False, unique=True),
    Column("description", String[250], nullable=False),
    Column("created_for", UUID(as_uuid=True), nullable=False),
    Column("updated_for", UUID(as_uuid=True), nullable=False),
    Column("created_at", DateTime, default=datetime.now()),
    Column("updated_at", DateTime, default=datetime.now(), onupdate=datetime.now),
)


mapper_registry.map_imperatively(
    Poomsae,
    poomsaes,
    properties={
        "bands": relationship(
            Band,
            secondary=band_poomsae,
            back_populates="poomsaes",
            cascade="all, delete",
        )
    },
)
