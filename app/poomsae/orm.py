from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, String, SmallInteger, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from app.poomsae.entities import Poomsae
from bootstrap.database import mapper_registry

poomsaes = Table(
    'poomsaes',
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String[50], nullable=False, unique=True),
    Column("description", String[250], nullable=False),
    Column("difficulty", SmallInteger, nullable=False),
    Column("fk_band", UUID(as_uuid=True), ForeignKey("bands.id"), default=uuid4),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, onupdate=datetime.utcnow)
)

mapper_registry.map_imperatively(Poomsae, poomsaes)
