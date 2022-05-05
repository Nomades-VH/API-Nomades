from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from app.band.repositories import AbstractBandRepository
from app.breakdown.repositories import (
    AbstractBreakdownRepository,
    AbstractBandBreakdownRepository,
)
from app.kibon_donjak.repositories import AbstractKibonDonjakRepository
from app.kick.repositories import AbstractKickRepository
from app.poomsae.repositories import AbstractPoomsaeRepository
from app.stretching.repositories import AbstractStretchingRepository
from app.theory.repositories import AbstractTheoryRepository
from app.user.repositories import AbstractUserRepository


class AbstractUow(ABC):
    band: AbstractBandRepository
    band_breakdown: AbstractBandBreakdownRepository
    breakdown: AbstractBreakdownRepository
    kibondonjak: AbstractKibonDonjakRepository
    kick: AbstractKickRepository
    poomsae: AbstractPoomsaeRepository
    stretching: AbstractStretchingRepository
    theory: AbstractTheoryRepository
    user: AbstractUserRepository

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
