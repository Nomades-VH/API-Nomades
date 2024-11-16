from abc import ABC
from typing import Optional, Iterator
from uuid import UUID

from app.user.entities import User
from ports.repository import AbstractRepository
from sqlalchemy import and_


class AbstractUserRepository(AbstractRepository[User], ABC):
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    def get_by_username(self, username: str) -> Optional[User]:
        pass

    def iter_include_inactive(self) -> Iterator[User]:
        ...

class UserRepository(AbstractUserRepository):
    def get(self, uuid: UUID) -> Optional[User]:
        return self.session.query(User).filter(and_(User.id == uuid, User.is_active)).first()

    def add(self, user: User) -> None:
        self.session.add(user)

    def update(self, user: User) -> None:
        update_data = user.to_dict(user)
        self.session.query(User).filter(User.id == user.id).update(update_data)

    def remove(self, uuid: UUID) -> None:
        self.session.query(User).filter(User.id == uuid).update({'is_activate': False})

    def iter(self) -> Iterator[User]:
        return self.session.query(User).filter(User.is_active).all()

    def iter_include_inactive(self) -> Iterator[User]:
        return self.session.query(User).all()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.session.query(User).filter(and_(User.email == email, User.is_active)).first()

    def get_by_username(self, username: str) -> Optional[User]:
        return self.session.query(User).filter(and_(User.username == username, User.is_active)).first()
