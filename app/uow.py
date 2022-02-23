from bootstrap.database import session_maker
from ports.uow import AbstractUow


class SqlAlchemyUow(AbstractUow):
    def __init__(self) -> None:
        super().__init__(session_factory=session_maker)

    def _open_session(self) -> None:
        self._session = self.session_factory()

    def _close_session(self) -> None:
        self._session.expunge_all()
        self._session.close()
        self._session.bind.dispose()

    def commit(self) -> None:
        self._session.commit()

    def rollback(self) -> None:
        self._session.rollback()
