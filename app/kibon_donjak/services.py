# TODO: Create a service for get_all KibonDonjaks
from dataclasses import asdict

from app.kibon_donjak.entities import KibonDonjak as KibonDonjakEntity
from app.kibon_donjak.models import KibonDonjak as KibonDonjakModel
from ports.uow import AbstractUow


def get(uow: AbstractUow):
    with uow:
        return list(map(asdict, uow.kibondonjak.iter()))


# TODO: Create a service for the get KiBonDonjak
def get_kibon_donjak():
    pass


def get_by_name(uow: AbstractUow, name):
    with uow:
        return uow.kibondonjak.get_by_name(name)


# TODO: Create a service for the post KiBonDonjak
def add(uow: AbstractUow, kibondonjak: KibonDonjakEntity):
    with uow:
        uow.kibondonjak.add(kibondonjak)


# TODO: Create a service for the put KiBonDonjak
def put_kibon_donjak():
    pass


# TODO: Create a service for the delete KiBonDonjak
def delete_kibon_donjak():
    pass
