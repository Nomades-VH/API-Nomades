from abc import ABC
from typing import Optional, Iterator
from uuid import UUID

from app.user.entities import User
from ports.repository import AbstractRepository


class AbstractUserRepository(AbstractRepository[User], ABC):
    pass


class UserRepository(AbstractUserRepository):

    def get(self, uuid: UUID) -> Optional[User]:
        return self.session.query(User).filter(User.id == uuid).first()

    def add(self, user: User) -> None:
        self.session.add(user)

    def update(self, user: User) -> None:
        self.session.query(User).filter(User.id == user.id).update(user)

    def remove(self, uuid: UUID) -> Optional[User]:
        return self.session.query(User).filter(User.id == uuid).delete()

    def iter(self) -> Iterator[User]:
        return self.session.query(User).all()
