from typing import Optional
from uuid import UUID as PyUUID

from sqlalchemy import UUID as SQLUUID
from sqlalchemy import Boolean, Column, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from general_enum.hubs import Hubs
from general_enum.permissions import Permissions
from ports.entity import Entity


class User(Entity):
    __tablename__ = 'users'  # Nome da tabela
    username: str = Column(String, unique=False, nullable=False)
    bio: str = Column(String, unique=False, nullable=True)
    email: str = Column(String, unique=True, nullable=False)
    password: str = Column(String, unique=False, nullable=False)
    permission: Permissions = Column(Enum(Permissions), nullable=False)
    src_profile: str = Column(String, unique=True, nullable=True)
    is_active: bool = Column(Boolean, nullable=False, default=False)
    hub: Hubs = Column(Enum(Hubs), nullable=False)
    fk_band: Optional[PyUUID] = Column(
        SQLUUID(as_uuid=True),
        ForeignKey('bands.id', ondelete='SET NULL'),
        nullable=True,
    )

    band = relationship('Band', back_populates='users')
    tokens = relationship('Auth', back_populates='user', uselist=False)


    @classmethod
    def to_dict(cls, user: 'User') -> dict:
        return {
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'permission': user.permission,
            'fk_band': user.fk_band,
            'src_profile': user.src_profile,
            'is_active': user.is_active,
            'created_at': user.created_at,
            'updated_at': user.updated_at,
        }

    @classmethod
    def from_dict(cls, user_dict: dict) -> 'User':
        return cls(
            username=user_dict['username'],
            email=user_dict['email'],
            password=user_dict['password'],
            permission=user_dict['permission'],
        )


# @dataclass
# class Exame(Entity):
#     fk_user: UUID
#     fk_band: UUID
#     note_poomsae: float
#     note_kibondonjak: float
#     note_kick: float
#     note_stretching: float
#     note_breakdown: float
#     note_theory: float
