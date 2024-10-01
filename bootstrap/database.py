import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

_URI = None

if "pytest" in sys.modules:
    _URI = os.environ.get('DATABASE_URI_TEST')
elif "alembic" in sys.modules:
    _URI = os.environ.get('DATABASE_URI_ALEMBIC_DEV')

if not _URI:
    _URI = os.environ.get('DATABASE_URI')

if not _URI:
    raise RuntimeError("Tente utilizar: export '$(cat .env | xargs)' ou atualizar o seu arquivo .env")


_engine = create_engine(_URI)
_Session = scoped_session(sessionmaker(bind=_engine, autoflush=True, expire_on_commit=False))


def session_maker() -> _Session:
    return _Session()


def ensure_all_entities():
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

    Base.metadata.create_all(bind=_engine)

    print('INICIANDO')
    for table in Base.metadata.tables.keys():
        print(f"value>: {table}")
