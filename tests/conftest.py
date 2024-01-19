import os
from typing import Generator
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, close_all_sessions

from app.uow import SqlAlchemyUow
from bootstrap.server import app
import pytest
from bootstrap.database import mapper_registry
from main import _create_root
from ports.uow import AbstractUow

base = mapper_registry


@pytest.fixture(scope="session")
def client() -> Generator:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="function")
def uow() -> SqlAlchemyUow:
    return SqlAlchemyUow()


@pytest.fixture(scope="session", autouse=True)
def create_root():
    uow = SqlAlchemyUow()
    _create_root(uow)


@pytest.fixture(scope="session", autouse=True)
def create_db() -> AbstractUow:
    engine = create_engine(os.environ.get("DATABASE_URI_TEST"))
    _Session = sessionmaker(bind=engine)

    # noinspection PyUnresolvedReferences
    import app.band.orm

    # noinspection PyUnresolvedReferences
    import app.theory.orm

    # noinspection PyUnresolvedReferences
    import app.breakdown.orm

    # noinspection PyUnresolvedReferences
    import app.kibon_donjak.orm

    # noinspection PyUnresolvedReferences
    import app.kick.orm

    # noinspection PyUnresolvedReferences
    import app.poomsae.orm

    # noinspection PyUnresolvedReferences
    import app.stretching.orm

    # noinspection PyUnresolvedReferences
    import app.user.orm

    # noinspection PyUnresolvedReferences
    import app.auth.orm
    base.metadata.create_all(engine)

    yield _Session(autoflush=True, expire_on_commit=False)

    close_all_sessions()
    base.metadata.drop_all(bind=engine)
