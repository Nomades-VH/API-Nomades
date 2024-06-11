# import uuid
# from dataclasses import asdict
# from uuid import uuid4
#
# from starlette.testclient import TestClient
#
# from app.band import services as sv
# from app.band.entities import Band
# from app.uow import SqlAlchemyUow
# from app.user.entities import User
# from tests.utils import band_valid, get_user_info
#
# invalid_uuid = uuid4()
# band = band_valid()
#
#
# def test_get(uow: SqlAlchemyUow) -> None:
#     response = list(map(asdict, sv.get(uow)))
#     assert response is not None
#     assert type(response) == list
#
#
# def test_get_by_uuid_with_not_exists_band(uow: SqlAlchemyUow) -> None:
#     response = sv.get_by_id(uow, invalid_uuid)
#     assert response is None
#
#
# def test_get_by_uuid_with_exists_band(uow: SqlAlchemyUow, client: TestClient) -> None:
#     user = User.from_dict(get_user_info(client))
#     entity = Band.from_dict(band, user)
#     entity.id = uuid.uuid4()
#     test = sv.add(uow, entity)
#     response = sv.get_by_id(uow, entity.id)
#     assert type(response) == Band
#     assert response.id == entity.id
#     assert response.name == entity.name
#     assert response.meaning == entity.meaning
#
#
# def test_post_band(uow: SqlAlchemyUow, client: TestClient) -> None:
#     user = User.from_dict(get_user_info(client))
#     entity = Band.from_dict(band, user)
#     entity.id = uuid.uuid4()
#     response = sv.add(uow, entity)
#
