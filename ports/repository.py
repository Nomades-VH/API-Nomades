from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Iterator
from uuid import UUID

from ports.entity import Entity

_T = TypeVar("_T", bound=Entity)

class AbstractRepository(Generic[_T], ABC):
    def __init__(self, session) -> None:
        self.session = session

    @abstractmethod
    def add(self, entity: _T) -> None:
        pass

    @abstractmethod
    def get(self, id: UUID) -> _T | None:
        pass

    @abstractmethod
    def remove(self, entity: _T) -> None:
        pass

    @abstractmethod
    def update(self, entity: _T) -> None:
        pass

    @abstractmethod
    def iter(self) -> Iterator[_T]:
        pass