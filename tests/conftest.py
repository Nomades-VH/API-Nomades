import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import close_all_sessions, sessionmaker

from app.uow import SqlAlchemyUow
from bootstrap.database import Base
from bootstrap.server import app
from main import _create_root
from ports.uow import AbstractUow
from tests.utils import get_authorization


@pytest.fixture(scope='class')
def client() -> TestClient:
    with TestClient(app) as c:
        c.headers = get_authorization(c)
        yield c


@pytest.fixture(scope='function')
def uow() -> SqlAlchemyUow:
    uow = SqlAlchemyUow()
    with uow:
        yield uow


@pytest.fixture(scope='session', autouse=True)
def create_root():
    uow = SqlAlchemyUow()
    _create_root(uow)


@pytest.fixture(scope='session', autouse=True)
def create_db() -> AbstractUow:
    engine = create_engine(os.environ.get('DATABASE_URI_TEST'))
    _Session = sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    # noinspection PyUnresolvedReferences
    import app.auth.entities
    import app.band.entities
    # noinspection PyUnresolvedReferences
    import app.kibon_donjak.entities
    # noinspection PyUnresolvedReferences
    import app.kick.entities
    # noinspection PyUnresolvedReferences
    import app.poomsae.entities
    # noinspection PyUnresolvedReferences
    import app.user.entities

    Base.metadata.create_all(engine)

    session = _Session(autoflush=True, expire_on_commit=False)

    yield session

    session.close()

    Base.metadata.drop_all(bind=engine)
