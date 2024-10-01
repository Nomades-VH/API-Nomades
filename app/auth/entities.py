from uuid import UUID as PyUUID
from sqlalchemy import Column, String, ForeignKey, Boolean, UUID as SQLUUID
from sqlalchemy.orm import relationship
from ports.entity import Entity

class Auth(Entity):
    __tablename__ = 'tokens'  # Nome da tabela
    access_token: str = Column(String, unique=True, nullable=False)
    fk_user: PyUUID = Column(SQLUUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    is_invalid: bool = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="tokens", uselist=False)

