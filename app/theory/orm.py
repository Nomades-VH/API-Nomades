from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.theory.entities import Theory
from bootstrap.database import mapper_registry

theory = Table(
    'theory',
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("description", String(200), nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, onupdate=datetime.utcnow)
)

mapper_registry.map_imperatively(Theory, theory)
