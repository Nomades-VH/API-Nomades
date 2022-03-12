from datetime import datetime
from uuid import uuid4

from sqlalchemy import Table, Column, DateTime, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.band.entities import Band
from app.breakdown.entities import Breakdown, BandBreakdown
from bootstrap.database import mapper_registry

breakdowns = Table(
    'breakdowns',
    mapper_registry.metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=uuid4),
    Column("name", String(50), nullable=False, unique=True),
    Column("description", String(150), nullable=False),
    Column("created_at", DateTime, default=datetime.utcnow),
    Column("updated_at", DateTime, onupdate=datetime.utcnow)
)

band_breakdown = Table(
    'band_breakdown',
    mapper_registry.metadata,
    Column("fk_band", UUID(as_uuid=True), ForeignKey('bands.id'), primary_key=True),
    Column("fk_breakdown", UUID(as_uuid=True), ForeignKey('breakdowns.id'), primary_key=True)
)

mapper_registry.map_imperatively(BandBreakdown, band_breakdown)
mapper_registry.map_imperatively(
    Breakdown,
    breakdowns,
    properties={
        'bands': relationship(
            Band,
            secondary=band_breakdown
        )
    }
)
