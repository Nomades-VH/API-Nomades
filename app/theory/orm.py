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

"""theory = Table(
    'theory_band',
    mapper_registry.metadata,
    Column("id_band", UUID(as_uuid=True), primary_key=True, ForeignKey('band.id'), nullable=False),
    Column("id_theory", UUID(as_uuid=True), primary_key=True, ForeignKey('theory.id'), nullable=False),
)
"""

"""mapper_registry.map_imperatively(
    Band, 
    band,
    properties={
        'theories': relationship(
            Theory,
            secondary=theory_band,
        ),
    }
)
"""