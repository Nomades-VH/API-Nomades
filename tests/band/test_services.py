from dataclasses import asdict
from uuid import uuid4

from starlette.testclient import TestClient

from app.band import services as sv
from app.band.entities import Band
from app.uow import SqlAlchemyUow
from app.user.entities import User
from tests.utils import band_valid, get_user_info

invalid_uuid = uuid4()


def test_get(uow: SqlAlchemyUow) -> None:
    response = list(map(asdict, sv.get(uow)))
    assert response is not None
    assert type(response) == list


def test_get_by_uuid_with_not_exists_band(uow: SqlAlchemyUow) -> None:
    response = sv.get_by_id(uow, invalid_uuid)
    assert response is None


def test_get_by_uuid_with_exists_band(uow: SqlAlchemyUow, client: TestClient) -> None:
    band = band_valid()
    user = User.from_dict(get_user_info(client))
    entity = Band.from_dict(band, user)
    sv.add(uow, entity)
    band_id = sv.get(uow)[0]['id']
    response = sv.get_by_id(uow, band_id)
    assert response.name == entity.name

# TODO: Precisaremos reformular todo o nosso código de controllers e services
#  Os serviços são responsáveis pela lógica de negócio, ou seja,
#  todo o tratamento de exceções, validação e etc.

# TODO: Talvez tenhamos que criar general_services também
