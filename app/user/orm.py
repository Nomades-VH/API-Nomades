from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.user.entities import User
from bootstrap.database import mapper_registry

users = Table(
    'users',
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String(50), nullable=False),
    Column("login", String(50), nullable=False, unique=True),
    Column("password", String(50), nullable=False),
    Column("fk_band", UUID(as_uuid=True), ForeignKey("bands.id"), default=uuid4),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, onupdate=datetime.utcnow)
)

mapper_registry.map_imperatively(User, users)
