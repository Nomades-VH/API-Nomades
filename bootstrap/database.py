from os import environ
from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker

mapper_registry = registry()

_POSTGRES_USER = environ.get("POSTGRES_USER")
_POSTGRES_PASSWORD = environ.get("POSTGRES_PASSWORD")
_POSTGRES_HOST = environ.get("POSTGRES_HOST")
_POSTGRES_PORT = environ.get("POSTGRES_PORT")
_POSTGRES_DATABASE = environ.get("POSTGRES_DB")

_POSTGRES_URI = f"postgresql+psycopg2://{_POSTGRES_USER}:{_POSTGRES_PASSWORD}@{_POSTGRES_HOST}:{_POSTGRES_PORT}/{_POSTGRES_DATABASE}"

_engine = create_engine(_POSTGRES_URI)
_Session = sessionmaker(bind=_engine)


def session_maker() -> _Session:
    return _Session(autoflush=True, expire_on_commit=False)


def ensure_all_entities():
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

    mapper_registry.metadata.create_all(bind=_engine)
