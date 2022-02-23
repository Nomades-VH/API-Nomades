from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, String, SmallInteger, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.kick.entities import Kick
from bootstrap.database import mapper_registry

kicks = Table(
    'kicks',
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String[50], nullable=False, unique=True),
    Column("description", String[250], nullable=False),
    Column("difficulty", SmallInteger, nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, onupdate=datetime.utcnow)
)

mapper_registry.map_imperatively(Kick, kicks)
