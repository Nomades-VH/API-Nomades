from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime

from app.band.entities import Band
from bootstrap.database import mapper_registry

bands = Table(
    "bands",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("gub", Integer, nullable=False, unique=True),
    Column("name", String(50), nullable=False, unique=True),
    Column("meaning", String(150), nullable=False),
    Column("created_for", String(50), nullable=False),
    Column("updated_for", String(50), nullable=False),
    Column("fk_theory", UUID(as_uuid=True), ForeignKey("theory.id"), default=uuid4),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, onupdate=datetime.utcnow),
)

mapper_registry.map_imperatively(Band, bands)
