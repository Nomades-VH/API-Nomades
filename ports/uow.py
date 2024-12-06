from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from app.auth.repositories import AbstractAuthRepository
from app.band.repositories import AbstractBandRepository
from app.kibon_donjak.repositories import AbstractKibonDonjakRepository
from app.kick.repositories import AbstractKickRepository
from app.poomsae.repositories import AbstractPoomsaeRepository
from app.user.repositories import AbstractUserRepository


class AbstractUow(ABC):
    band: AbstractBandRepository
    kibondonjak: AbstractKibonDonjakRepository
    kick: AbstractKickRepository
    poomsae: AbstractPoomsaeRepository
    user: AbstractUserRepository
    auth: AbstractAuthRepository

    def __init__(self, session_factory: Callable[[], Any]):
        self.session_factory = session_factory

    def __enter__(self) -> None:
        self._open_session()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type is None:
            self.commit()
        else:
            self.rollback()

        self._close_session()

    @abstractmethod
    def _open_session(self) -> None:
        pass

    @abstractmethod
    def _close_session(self) -> None:
        pass

    @abstractmethod
    def commit(self) -> None:
        pass

    @abstractmethod
    def rollback(self) -> None:
        pass
