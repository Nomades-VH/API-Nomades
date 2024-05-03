from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.band.entities import Band
from app.band.orm import band_kick
from app.kick.entities import Kick
from bootstrap.database import mapper_registry


kicks = Table(
    "kicks",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String[100], nullable=False, unique=True),
    Column("description", String[250], nullable=False),
    Column("created_for", UUID(as_uuid=True), nullable=False),
    Column("updated_for", UUID(as_uuid=True), nullable=False),
    Column("created_at", DateTime, default=datetime.now()),
    Column("updated_at", DateTime, default=datetime.now(), onupdate=datetime.now),
)

mapper_registry.map_imperatively(Kick, kicks, properties={
    "bands": relationship(
        Band,
        secondary=band_kick,
        back_populates="kicks",
        cascade="all, delete"
    )
})
