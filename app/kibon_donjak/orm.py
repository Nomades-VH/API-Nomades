from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, String, DateTime, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.band.entities import Band
from app.band.orm import band_kibondonjak
from app.kibon_donjak.entities import KibonDonjak
from bootstrap.database import mapper_registry

kibon_donjak = Table(
    "kibon_donjaks",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String(50), nullable=False, unique=True),
    Column("description", String(255), nullable=False),
    Column("created_for", UUID(as_uuid=True), nullable=False),
    Column("updated_for", UUID(as_uuid=True), nullable=False),
    Column("fk_band", UUID(as_uuid=True), ForeignKey("bands.id", ondelete='CASCADE'), nullable=False),
    Column("created_at", DateTime, default=datetime.now()),
    Column("updated_at", DateTime, default=datetime.now(), onupdate=datetime.now),
)


mapper_registry.map_imperatively(KibonDonjak, kibon_donjak, properties={
    "bands": relationship(
        Band,
        secondary=band_kibondonjak,
        back_populates="kibon_donjaks",
        cascade="all, delete"
    )
})