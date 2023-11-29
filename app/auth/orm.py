from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Table, Column, String, ForeignKey, DateTime, Boolean

from app.auth.entities import Auth
from bootstrap.database import mapper_registry

tokens = Table(
    "tokens",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("access_token", String(250), unique=True, nullable=False),
    Column("is_invalid", Boolean, nullable=False, default=False),
    Column("fk_user", UUID(as_uuid=True), ForeignKey("users.id"), default=uuid4),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
)

mapper_registry.map_imperatively(Auth, tokens)
