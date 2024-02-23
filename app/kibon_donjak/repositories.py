import dataclasses
from abc import ABC
from typing import Iterator, Optional
from uuid import UUID

from sqlalchemy import desc

from app.kibon_donjak.entities import KibonDonjak
from ports.repository import AbstractRepository


class AbstractKibonDonjakRepository(AbstractRepository[KibonDonjak], ABC):
    def get_by_name(self, name: str) -> Optional[KibonDonjak]:
        ...


# TODO: Verificar todos os métodos
class KibonDonjakRepository(AbstractKibonDonjakRepository):

    def get(self, uuid: UUID) -> Optional[KibonDonjak]:
        return self.session.query(KibonDonjak).filter(KibonDonjak.id == uuid).first()

    def get_by_name(self, name: str) -> Optional[KibonDonjak]:
        return self.session.query(KibonDonjak).filter(KibonDonjak.name == name).first()

    def add(self, kibon_donjak: KibonDonjak) -> None:
        self.session.add(kibon_donjak)

    def remove(self, uuid: UUID) -> Optional[KibonDonjak]:
        return self.session.query(KibonDonjak).filter(KibonDonjak.id == uuid).delete()

    def update(self, kibon_donjak: KibonDonjak) -> None:
        self.session.query(KibonDonjak).filter(
            KibonDonjak.id == kibon_donjak.id
        ).update(dataclasses.asdict(kibon_donjak))

    def iter(self) -> Iterator[KibonDonjak]:
        return self.session.query(KibonDonjak).order_by(KibonDonjak.created_at).all()
