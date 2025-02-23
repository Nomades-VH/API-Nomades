import dataclasses
from abc import ABC
from typing import List, Optional
from uuid import UUID

from sqlalchemy import and_

from app.auth.entities import Auth
from app.user.entities import User
from ports.repository import AbstractRepository


class AbstractAuthRepository(AbstractRepository[Auth], ABC):
    def get_by_user(self, uuid: UUID) -> Optional[Auth]:
        ...

    def get_by_token(self, token: str) -> Optional[Auth]:
        ...

    def update_from_user(self, entity: Auth, user_id: UUID) -> None:
        ...


class AuthRepository(AbstractAuthRepository):
    def add(self, entity: Auth) -> None:
        self.session.add(entity)

    def get(self, uuid: UUID) -> Optional[Auth]:
        return self.session.query(Auth).filter(Auth.id == uuid).first()

    def get_by_user(self, uuid: UUID) -> Optional[Auth]:
        return self.session.query(Auth).filter(Auth.fk_user == uuid).first()

    def get_by_token(self, token: str) -> Optional[Auth]:
        return (
            self.session.query(Auth).filter(and_(Auth.access_token == token, User.is_active == True)).first()
        )

    def remove(self, token: str) -> Optional[Auth]:
        ...

    def update(self, entity: Auth) -> None:
        update_data = {
            key: value
            for key, value in entity.__dict__.items()
            if not key.startswith('_')
        }

        self.session.query(Auth).filter(Auth.id == entity.id).update(
            update_data
        )

    def update_from_user(self, entity: Auth, user_id: UUID) -> None:
        update_data = {
            key: value
            for key, value in entity.__dict__.items()
            if not key.startswith('_')
        }

        self.session.query(Auth).filter(Auth.fk_user == user_id).update(
            update_data
        )

    def iter(self) -> List[Auth]:
        return self.session.query(Auth).filter(Auth.is_invalid == False).all()
