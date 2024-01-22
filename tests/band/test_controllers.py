from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.utils import get_authorization_headers, band_valid, get_band_by_gub

message_create_error = "Faixa não encontrada."
message_update_error = "Faixa não atualizada."
invalid_uuid = "f7f00446-6d6a-417c-82e5-33a0698af17b"
url = "/band/"


def test_get_bands(client: TestClient):
    authorization = get_authorization_headers(client)
    response = client.get(url, headers=authorization)
    assert response.status_code == HTTPStatus.OK
    assert response.json()["message"] == "Não foram encontradas faixas."


def test_post_band(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    response = client.post(url, json=band, headers=authorization)
    assert response.status_code == HTTPStatus.OK
    band_created = get_band_by_gub(band['gub'], authorization, client)
    assert band_created['name'] == band['name']


def test_post_existing_gub_band(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    client.post(url, json=band, headers=authorization)
    response = client.post(url, json=band, headers=authorization)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['message'] == f"Gub {band['gub']} já existe."


def test_post_existing_name_band(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    client.post(url, json=band, headers=authorization)
    band['gub'] += 1
    response = client.post(url, json=band, headers=authorization)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['message'] == f"{band['name']} já existe."


def test_post_with_wrong_gub(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    band['gub'] = 'wrong'
    response = client.post(url, json=band, headers=authorization)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['message'] == "Argumento inválido ou ausência de argumentos.: gub"


def test_post_with_wrong_name(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    band['name'] = 2
    response = client.post(url, json=band, headers=authorization)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['message'] == "Argumento inválido ou ausência de argumentos.: name"


def test_post_band_with_wrong_meaning(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    band['meaning'] = 1
    response = client.post(url, json=band, headers=authorization)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['message'] == "Argumento inválido ou ausência de argumentos.: meaning"


def test_post_band_without_arguments(client: TestClient):
    authorization = get_authorization_headers(client)
    response = client.post(url, json={}, headers=authorization)
    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['message'] == "Argumento inválido ou ausência de argumentos.: gub"


def test_get_by_id(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    client.post(url, json=band, headers=authorization)
    band = client.get(url, headers=authorization).json()[0]
    response = client.get(f'{url}{band['id']}', headers=authorization)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == band


def test_get_by_gub(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    client.post(url, json=band, headers=authorization)
    band_caught = client.get(url, headers=authorization).json()[0]
    response = client.get(f'{url}gub/{band['gub']}', headers=authorization)
    assert response.status_code == HTTPStatus.OK
    assert response.json() == band_caught


def test_get_by_gub_not_found(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    client.post(url, json=band, headers=authorization)
    response = client.get(f'{url}gub/{band['gub'] + 1}', headers=authorization)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['message'] == message_create_error


def test_get_by_id_not_found(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    client.post(url, json=band, headers=authorization)
    response = client.get(f'{url}{invalid_uuid}', headers=authorization)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['message'] == message_create_error


def test_update_band_not_found(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    response = client.put(f"{url}{invalid_uuid}", json=band, headers=authorization)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['message'] == message_update_error


def test_update_band(client: TestClient):
    authorization = get_authorization_headers(client)
    band = band_valid()
    client.post(url, json=band, headers=authorization)
    band_caught = client.get(f'{url}gub/{band['gub']}', headers=authorization)
    band['name'] = "new name"
    response = client.put(f"{url}{band_caught.json()['id']}", json=band, headers=authorization)
    assert response.status_code == HTTPStatus.OK
    new_band_caught = client.get(f'{url}{band_caught.json()["id"]}', headers=authorization)
    assert new_band_caught.json()['name'] == band['name']


def test_delete_band_not_found(client: TestClient):
    authorization = get_authorization_headers(client)
    response = client.delete(f"{url}{invalid_uuid}", headers=authorization)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['message'] == message_create_error


def test_delete_band(client: TestClient):
    autorization = get_authorization_headers(client)
    band = band_valid()
    client.post(url, json=band, headers=autorization)
    uuid = client.get(url, headers=autorization).json()[0]['id']
    response = client.delete(f"{url}{uuid}", headers=autorization)
    assert response.status_code == HTTPStatus.OK
    response = client.get(url, headers=autorization).json()
    assert response["message"] == "Não foram encontradas faixas."
