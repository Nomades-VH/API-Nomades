from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Table, Column, String, DateTime, SmallInteger
from sqlalchemy.dialects.postgresql import UUID

from app.stretching.entities import Stretching
from bootstrap.database import mapper_registry

stretchings = Table(
    "stretchings",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String(50), nullable=False, unique=True),
    Column("description", String(250), nullable=False),
    Column("difficulty", SmallInteger, nullable=False),
    Column("created_at", DateTime, default=datetime.now(timezone.utc)),
    Column("updated_at", DateTime, onupdate=datetime.now(timezone.utc)),
)

mapper_registry.map_imperatively(Stretching, stretchings)
