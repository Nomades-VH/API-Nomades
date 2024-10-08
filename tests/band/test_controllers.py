from http import HTTPStatus

from fastapi.testclient import TestClient

from tests.utils import band_valid, get_band_by_gub, invalid_uuid

message_create_error = "Faixa não encontrada."
message_update_error = "Faixa não atualizada."
url = "/band/"


class TestBand:
    def test_get_bands_without_bands(self, client: TestClient):
        response = client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["message"] == "Não foram encontradas faixas."

    def test_post_band(self, client: TestClient):
        band = band_valid()
        response = client.post(url, json=band)
        assert response.status_code == HTTPStatus.OK
        band_created = get_band_by_gub(band["gub"], client)
        assert band_created["name"] == band["name"]

    def test_get_bands(self, client: TestClient):
        band = band_valid()
        client.post(url, json=band)
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert type(response.json()) == list
        assert len(response.json()) > 0
        assert response.json()[0]["name"] == band["name"]

    def test_post_existing_gub_band(self, client: TestClient):
        band = band_valid()
        client.post(url, json=band)
        response = client.post(url, json=band)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["message"] == f"Gub {band['gub']} já existe."

    def test_post_existing_name_band(self, client: TestClient):
        band = band_valid()
        client.post(url, json=band)
        band["gub"] += 1
        response = client.post(url, json=band)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["message"] == f"{band['name']} já existe."

    def test_post_with_wrong_gub(self, client: TestClient):
        band = band_valid()
        band["gub"] = "wrong"
        response = client.post(url, json=band)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            response.json()["message"]
            == "Argumento inválido ou ausência de argumentos.: gub"
        )

    def test_post_with_wrong_name(self, client: TestClient):
        band = band_valid()
        band["name"] = 2
        response = client.post(url, json=band)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            response.json()["message"]
            == "Argumento inválido ou ausência de argumentos.: name"
        )

    def test_post_band_with_wrong_meaning(self, client: TestClient):
        band = band_valid()
        band["meaning"] = 1
        response = client.post(url, json=band)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            response.json()["message"]
            == "Argumento inválido ou ausência de argumentos.: meaning"
        )

    def test_post_band_without_arguments(self, client: TestClient):
        response = client.post(url, json={})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            response.json()["message"]
            == "Argumento inválido ou ausência de argumentos.: gub"
        )

    def test_get_by_id(self, client: TestClient):
        band = band_valid()
        client.post(url, json=band)
        band = client.get(url).json()[0]
        response = client.get(f"{url}{band['id']}")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == band

    def test_get_by_gub(self, client: TestClient):
        band = band_valid()
        client.post(url, json=band)
        band_caught = client.get(url).json()[0]
        response = client.get(f"{url}gub/{band['gub']}")
        assert response.status_code == HTTPStatus.OK
        assert response.json() == band_caught

    def test_get_by_gub_not_found(self, client: TestClient):
        band = band_valid()
        client.post(url, json=band)
        response = client.get(f"{url}gub/{band['gub'] + 1}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["message"] == message_create_error

    def test_get_by_id_not_found(self, client: TestClient):
        band = band_valid()
        client.post(url, json=band)
        response = client.get(f"{url}{invalid_uuid}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["message"] == message_create_error

    def test_update_band_not_found(self, client: TestClient):
        band = band_valid()
        response = client.put(f"{url}{invalid_uuid}", json=band)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert (
            response.json()["message"] == message_update_error + " ID não encontrado."
        )

    def test_update_band(self, client: TestClient):
        band = band_valid()
        client.post(url, json=band)
        band_caught = client.get(f"{url}gub/{band['gub']}")
        band["name"] = "new name"
        response = client.put(f"{url}{band_caught.json()['id']}", json=band)
        assert response.status_code == HTTPStatus.OK
        new_band_caught = client.get(f'{url}{band_caught.json()["id"]}')
        assert new_band_caught.json()["name"] == band["name"]
        assert new_band_caught.json()["updated_at"] != band_caught.json()["updated_at"]

    def test_delete_band_not_found(self, client: TestClient):
        response = client.delete(f"{url}{invalid_uuid}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["message"] == message_create_error

    def test_delete_band(self, client: TestClient):
        band = band_valid()
        client.post(url, json=band)
        uuid = client.get(url).json()[0]["id"]
        response = client.delete(f"{url}{uuid}")
        assert response.status_code == HTTPStatus.OK
        response = client.get(url).json()
        assert response["message"] == "Não foram encontradas faixas."
