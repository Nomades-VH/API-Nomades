from abc import ABC
from typing import Iterator, List, Optional
from uuid import UUID

from sqlalchemy import and_

from app.user.entities import User
from ports.repository import AbstractRepository


class AbstractUserRepository(AbstractRepository[User], ABC):
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    def get_by_username(self, username: str) -> Optional[User]:
        pass

    def iter_include_inactive(self) -> List[User]:
        ...

    def iter_only_deactivates(self) -> List[User]:
        ...


class UserRepository(AbstractUserRepository):
    def get(self, uuid: UUID) -> Optional[User]:
        return (
            self.session.query(User)
            .filter(and_(User.id == uuid, User.is_active))
            .first()
        )

    def add(self, user: User) -> None:
        self.session.add(user)

    def update(self, user: User) -> None:
        update_data = user.to_dict(user)
        self.session.query(User).filter(User.id == user.id).update(update_data)

    def remove(self, uuid: UUID) -> None:
        self.session.query(User).filter(User.id == uuid).update(
            {'is_activate': False}
        )

    def iter(self) -> Iterator[User]:
        return self.session.query(User).filter(User.is_active).all()

    def iter_include_inactive(self) -> List[User]:
        return self.session.query(User).all()

    def iter_only_deactivates(self) -> List[User]:
        return self.session.query(User).filter(User.is_active == False).all()

    def get_by_email(self, email: str) -> Optional[User]:
        return (
            self.session.query(User)
            .filter(and_(User.email == email, User.is_active))
            .first()
        )

    def get_by_username(self, username: str) -> Optional[User]:
        return (
            self.session.query(User)
            .filter(and_(User.username == username, User.is_active))
            .first()
        )
