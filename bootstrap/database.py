import os
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import registry, sessionmaker

mapper_registry = registry()

_URI = None

if "pytest" in sys.modules:
    _URI = os.environ.get('DATABASE_URI_TEST')
elif "alembic" in sys.modules:
    _URI = os.environ.get('DATABASE_URI_ALEMBIC')

if not _URI:
    _URI = os.environ.get('DATABASE_URI')

if not _URI:
    raise RuntimeError("Tente utilizar: export '$(cat .env | xargs)' ou atualizar o seu arquivo .env")


_engine = create_engine(_URI)
_Session = sessionmaker(bind=_engine)


def session_maker() -> _Session:
    return _Session(autoflush=True, expire_on_commit=False)


def ensure_all_entities():
    # noinspection PyUnresolvedReferences
    import app.band.orm

    # noinspection PyUnresolvedReferences
    import app.kibon_donjak.orm

    # noinspection PyUnresolvedReferences
    import app.kick.orm

    # noinspection PyUnresolvedReferences
    import app.poomsae.orm

    # noinspection PyUnresolvedReferences
    import app.user.orm

    # noinspection PyUnresolvedReferences
    import app.auth.orm

    mapper_registry.metadata.reflect(bind=_engine)
