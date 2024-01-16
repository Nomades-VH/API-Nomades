from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, String, DateTime, SmallInteger
from sqlalchemy.dialects.postgresql import UUID

from app.kibon_donjak.entities import KibonDonjak
from bootstrap.database import mapper_registry

kibon_donjak = Table(
    "kibon_donjaks",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String(50), nullable=False, unique=True),
    Column("description", String(255), nullable=False),
    Column("difficulty", SmallInteger, nullable=False),
    Column("created_at", DateTime, default=datetime.now()),
    Column("updated_at", DateTime, onupdate=datetime.now()),
)

mapper_registry.map_imperatively(KibonDonjak, kibon_donjak)
