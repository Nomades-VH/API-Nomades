from app.auth.repositories import AuthRepository
from app.band.repositories import BandRepository
from app.kibon_donjak.repositories import KibonDonjakRepository
from app.kick.repositories import KickRepository
from app.poomsae.repositories import PoomsaeRepository
from app.user.repositories import UserRepository
from bootstrap.database import session_maker
from ports.uow import AbstractUow


class SqlAlchemyUow(AbstractUow):
    def __init__(self) -> None:
        super().__init__(session_factory=session_maker)

    def _open_session(self) -> None:
        self._session = self.session_factory()
        self.band = BandRepository(self._session)
        self.kibondonjak = KibonDonjakRepository(self._session)
        self.kick = KickRepository(self._session)
        self.poomsae = PoomsaeRepository(self._session)
        self.user = UserRepository(self._session)
        self.auth = AuthRepository(self._session)

    def _close_session(self) -> None:
        self._session.expunge_all()
        self._session.close()
        self._session.bind.dispose()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
