import os
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions

from app.uow import SqlAlchemyUow
from bootstrap.server import app
import pytest
from bootstrap.database import Base
from main import _create_root
from ports.uow import AbstractUow


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def uow() -> SqlAlchemyUow:
    uow = SqlAlchemyUow()
    with uow:
        yield uow


@pytest.fixture(scope="session", autouse=True)
def create_root():
    uow = SqlAlchemyUow()
    _create_root(uow)


@pytest.fixture(scope="session", autouse=True)
def create_db() -> AbstractUow:
    engine = create_engine(os.environ.get("DATABASE_URI_TEST"))
    _Session = sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import app.band.entities

    # noinspection PyUnresolvedReferences
    import app.kibon_donjak.entities

    # noinspection PyUnresolvedReferences
    import app.kick.entities

    # noinspection PyUnresolvedReferences
    import app.poomsae.entities

    # noinspection PyUnresolvedReferences
    import app.user.entities

    # noinspection PyUnresolvedReferences
    import app.auth.entities
    Base.metadata.create_all(engine)

    yield _Session(autoflush=True, expire_on_commit=False)

    close_all_sessions()
    Base.metadata.drop_all(bind=engine)
