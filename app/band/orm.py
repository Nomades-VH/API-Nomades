from datetime import datetime
from uuid import uuid4

from sqlalchemy.dialects.postgresql import UUID

from sqlalchemy import Table, Column, Integer, String, DateTime, Index, ForeignKey
from sqlalchemy.orm import relationship

from app.band.entities import Band
from app.kibon_donjak.entities import KibonDonjak
from app.kick.entities import Kick
from app.poomsae.entities import Poomsae
from bootstrap.database import mapper_registry

bands = Table(
    "bands",
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("gub", Integer, nullable=False, unique=True),
    Column("name", String(50), nullable=False, unique=True),
    Column("meaning", String(600), nullable=False),
    Column("theory", String(600), nullable=False),
    Column("breakdown", String(600), nullable=False),
    Column("stretching", String(600), nullable=False),
    Column("created_for", UUID(as_uuid=True), nullable=False),
    Column("updated_for", UUID(as_uuid=True), nullable=False),
    Column("created_at", DateTime, default=datetime.now()),
    Column("updated_at", DateTime, default=datetime.now(), onupdate=datetime.now),
)

created_updated_for_index = Index('idx_created_updated_for', bands.c.created_for, bands.c.updated_for)
gub_index = Index('idx_gub', bands.c.gub)
created_updated_at_index = Index('idx_created_updated_at', bands.c.created_at, bands.c.updated_at)

band_kick = Table(
    "band_kick",
    mapper_registry.metadata,
    Column("band_id", UUID(as_uuid=True), ForeignKey("bands.id", ondelete="CASCADE"), primary_key=True, nullable=False),
    Column("kick_id", UUID(as_uuid=True), ForeignKey("kicks.id", ondelete="CASCADE"), primary_key=True, nullable=False),
)

band_poomsae = Table(
    "band_poomsae",
    mapper_registry.metadata,
    Column("band_id", UUID(as_uuid=True), ForeignKey("bands.id", ondelete="CASCADE"), primary_key=True, nullable=False),
    Column("poomsae_id", UUID(as_uuid=True), ForeignKey("poomsaes.id", ondelete="CASCADE"), primary_key=True, nullable=False),
)

band_kibondonjak = Table(
    "band_kibondonjak",
    mapper_registry.metadata,
    Column("band_id", UUID(as_uuid=True), ForeignKey("bands.id", ondelete="CASCADE"), primary_key=True, nullable=False),
    Column("kibondonjak_id", UUID(as_uuid=True), ForeignKey("kibon_donjaks.id", ondelete="CASCADE"), primary_key=True, nullable=False),
)

mapper_registry.map_imperatively(Band, bands, properties={
    # Preciso criar uma relação com as tabelas kicks, poomsaes e kibon_donjaks
    "kicks": relationship(
        Kick,
        secondary=band_kick,
        back_populates="bands",
        cascade="all, delete",
        lazy='joined'
    ),
    "poomsaes": relationship(
        Poomsae,
        secondary=band_poomsae,
        back_populates="bands",
        cascade="all, delete",
        lazy='joined'
    ),
    "kibon_donjaks": relationship(
        KibonDonjak,
        secondary=band_kibondonjak,
        back_populates="bands",
        cascade="all, delete",
        lazy='joined'
    )
})
