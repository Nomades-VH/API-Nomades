from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, String, ForeignKey, DateTime, Float, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.band.entities import Band
from app.user.entities import User, Exame
from bootstrap.database import mapper_registry
from general_enum.permissions import Permissions

users = Table(
    "users",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("username", String(50), nullable=False),
    Column("email", String(50), nullable=False, unique=True),
    Column("password", String(100), nullable=False),
    Column("permission", Enum(Permissions), nullable=False),
    Column("fk_band", UUID(as_uuid=True), ForeignKey("bands.id", ondelete='SET NULL')),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, default=datetime.utcnow, onupdate=datetime.utcnow),
)

exame = Table(
    "exame",
    mapper_registry.metadata,
    Column("fk_user", UUID(as_uuid=True), ForeignKey("users.id", ondelete='CASCADE'), primary_key=True),
    Column("fk_band", UUID(as_uuid=True), ForeignKey("bands.id", ondelete='CASCADE'), nullable=True),
    Column("note_poomsae", Float),
    Column("note_kibondonjak", Float),
    Column("note_kick", Float),
    Column("note_stretching", Float),
    Column("note_breakdown", Float),
    Column("note_theory", Float),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("exame_date_at", DateTime, onupdate=datetime.utcnow),
)

mapper_registry.map_imperatively(Exame, exame)
mapper_registry.map_imperatively(
    User,
    users,
    properties={
        "bands": relationship(
            Band,
            secondary=exame,
        )
    },
)
