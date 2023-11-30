import dataclasses
from abc import ABC
from typing import Iterator, Optional
from uuid import UUID

from sqlalchemy import and_

from app.auth.entities import Auth
from ports.repository import AbstractRepository


class AbstractAuthRepository(AbstractRepository[Auth], ABC):
    def get_by_user(self, uuid: UUID) -> Optional[Auth]:
        ...

    def get_by_token(self, token: str) -> Optional[Auth]:
        ...


class AuthRepository(AbstractAuthRepository):

    def add(self, entity: Auth) -> None:
        self.session.add(entity)

    def get(self, uuid: UUID) -> Optional[Auth]:
        return self.session.query(Auth).filter(and_(Auth.id == uuid, not Auth.is_invalid == False)).first()

    def get_by_user(self, uuid: UUID) -> Optional[Auth]:
        return self.session.query(Auth).filter(and_(Auth.fk_user == uuid, Auth.is_invalid == False)).first()

    def get_by_token(self, token: str) -> Optional[Auth]:
        return self.session.query(Auth).filter(and_(Auth.access_token == token, Auth.is_invalid == False)).first()

    def remove(self, token: str) -> Optional[Auth]:
        ...

    def update(self, entity: Auth) -> None:
        self.session.query(Auth).filter(Auth.id == entity.id).update(dataclasses.asdict(entity))

    def iter(self) -> Iterator[Auth]:
        pass
