from dataclasses import field
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.declarative import as_declarative
from sqlalchemy.dialects.postgresql import UUID as SQLUUID
from sqlalchemy.orm import declared_attr
from bootstrap.database import Base

@as_declarative()
class Entity(Base):
    __abstract__ = True  # Define como classe abstrata, para que não seja criada diretamente
    id: UUID = field(init=False)
    created_at: datetime = field(init=False)
    updated_at: datetime = field(init=False)
    created_for: Optional[UUID] = field(init=False)
    updated_for: Optional[UUID] = field(init=False)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @declared_attr
    def id(cls):
        return Column(SQLUUID(as_uuid=True), primary_key=True, default=uuid4)

    @declared_attr
    def created_at(cls):
        return Column(DateTime, default=datetime.now())

    @declared_attr
    def updated_at(cls):
        return Column(DateTime, default=datetime.now(), onupdate=datetime.now())

    @declared_attr
    def created_for(cls):
        return Column(SQLUUID(as_uuid=True), nullable=True)

    @declared_attr
    def updated_for(cls):
        return Column(SQLUUID(as_uuid=True), nullable=True)

    def __hash__(self) -> int:
        return hash(self.id)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Entity):
            return False

        return self.id == other.id

    def __init_subclass__(cls):
        super().__init_subclass__()
        if cls.__name__ != "Entity":
            cls.metadata = Base.metadata