from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from ports.entity import Entity

_T = TypeVar('_T', bound=Entity)


class AbstractRepository(Generic[_T], ABC):
    def __init__(self, session) -> None:
        self.session = session

    @abstractmethod
    def add(self, entity: _T):
        pass

    @abstractmethod
    def get(self, id: UUID) -> Optional[_T]:
        pass

    @abstractmethod
    def remove(self, uuid: UUID) -> Optional[_T]:
        pass

    @abstractmethod
    def update(self, entity: _T) -> None:
        pass

    @abstractmethod
    def iter(self) -> List[_T]:
        pass
