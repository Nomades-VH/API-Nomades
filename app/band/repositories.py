import dataclasses
from abc import ABC
from typing import Optional, List
from uuid import UUID

from sqlalchemy import desc
from sqlalchemy.orm import joinedload

from app.band.entities import Band
from app.kibon_donjak.entities import KibonDonjak
from ports.repository import AbstractRepository


def convert_uuid_to_string(data):
    if isinstance(data, UUID):
        dated = str(data)
        return dated
    elif isinstance(data, dict):
        return {k: convert_uuid_to_string(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_uuid_to_string(item) for item in data]
    else:
        return data


class AbstractBandRepository(AbstractRepository[Band], ABC):
    def get_by_gub(self, gub: int) -> Optional[Band]:
        pass

    def get_by_name(self, name: str) -> Optional[Band]:
        pass

    def remove_by_name(self, name: str) -> Optional[Band]:
        pass


class BandRepository(AbstractBandRepository):
    def get(self, band_id: UUID):
        return (self.session.query(Band)
                .filter_by(id=band_id).one_or_none())

    def get_by_gub(self, gub: int) -> Optional[Band]:
        return self.session.query(Band).filter(Band.gub == gub).first()

    def get_by_name(self, name: str) -> Optional[Band]:
        return self.session.query(Band).filter(Band.name == name).first()

    def add(self, band: Band) -> None:
        self.session.add(band)

    def remove(self, uuid: UUID) -> Optional[Band]:
        return self.session.query(Band).filter(Band.id == uuid).delete()

    def update(self, band: Band) -> None:
        band = {
            k: v
            for k, v in band.__dict__.items()
            if k not in ["kicks", "poomsaes", "kibon_donjaks", "_sa_instance_state"]
        }
        self.session.query(Band).filter(Band.id == band["id"]).update(band)

    def iter(self) -> List[Band]:
        return self.session.query(Band).order_by(desc(Band.gub)).all()

    # TODO: Create a method to remove band with name
    def remove_by_name(self, name: str) -> Optional[Band]:
        pass
