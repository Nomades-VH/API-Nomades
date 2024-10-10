from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.utils import kibon_donjak_valid, get_kibon_donjak_by_id, invalid_uuid

message_get_error = "Não foi encontrado o Kibon Donjak."
message_update_error = "Não foi possível atualizar o Kibon Donjak."
message_delete_error = "Não foi possível deletar o Kibon Donjak."

url = "/kibon_donjak/"


class TestKibonDonjak:

    @pytest.fixture(scope="function")
    def kibon_donjak(self):
        return kibon_donjak_valid()  # Retorna a variável kibon_donjak

    def test_get_kibon_donjaks_without_kibon_donjaks(self, client: TestClient):
        response = client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["message"] == "Não foram encontrados Kibon Donjaks."

    def test_post_kibon_donjak(self, client: TestClient, kibon_donjak):
        response = client.post(url, json=kibon_donjak)
        assert response.status_code == HTTPStatus.OK
        kibon_donjak_created = get_kibon_donjak_by_id(response.json()["id"], client)
        assert kibon_donjak_created["name"] == kibon_donjak["name"]

    def test_get_kibon_donjaks(self, client: TestClient, kibon_donjak):
        client.post(url, json=kibon_donjak)
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert type(response.json()) == list
        assert len(response.json()) > 0
        assert response.json()[0]["name"] == kibon_donjak["name"]

    def test_post_kibon_donjak_existing_name(self, client: TestClient, kibon_donjak):
        client.post(url, json=kibon_donjak)
        response = client.post(url, json=kibon_donjak)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert response.json()["message"] == f"{kibon_donjak['name']} já existe."

    def test_post_kibon_donjak_with_wrong_name(self, client: TestClient, kibon_donjak):
        kibon_donjak["name"] = None
        response = client.post(url, json=kibon_donjak)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            response.json()["message"]
            == "Argumento inválido ou ausência de argumentos.: name"
        )

    def test_post_kibon_donjak_with_wrong_meaning(self, client: TestClient, kibon_donjak):
        kibon_donjak["description"] = None
        response = client.post(url, json=kibon_donjak)
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            response.json()["message"]
            == "Argumento inválido ou ausência de argumentos.: description"
        )

    def test_post_band_without_arguments(self, client: TestClient):
        response = client.post(url, json={})
        assert response.status_code == HTTPStatus.BAD_REQUEST
        assert (
            response.json()["message"]
            == "Argumento inválido ou ausência de argumentos.: name"
        )

    def test_get_by_id(self, client: TestClient, kibon_donjak):
        client.post(url, json=kibon_donjak)
        kibon_donjak = client.get(url).json()[0]
        response = client.get(f'{url}{kibon_donjak["id"]}')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == kibon_donjak

    def test_get_by_id_not_found(self, client: TestClient, kibon_donjak):
        client.post(url, json=kibon_donjak)
        response = client.get(f"{url}{invalid_uuid}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["message"] == message_get_error

    def test_update_band_not_found(self, client: TestClient, kibon_donjak):
        response = client.put(f"{url}{invalid_uuid}", json=kibon_donjak)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert (
            response.json()["message"]
            == message_update_error + " ID não encontrado."
        )

    def test_update_band(self, client: TestClient, kibon_donjak):
        client.post(url, json=kibon_donjak)
        kibon_donjak_caught = client.get(url).json()[0]
        kibon_donjak["name"] = "new name"
        response = client.put(f"{url}{kibon_donjak_caught['id']}", json=kibon_donjak)
        assert response.status_code == HTTPStatus.OK
        new_kibon_donjak_caught = client.get(f'{url}{kibon_donjak_caught["id"]}')
        assert new_kibon_donjak_caught.json()["name"] == kibon_donjak["name"]
        assert (
            new_kibon_donjak_caught.json()["updated_at"] != kibon_donjak_caught["updated_at"]
        )

    def test_delete_kibon_donjak_not_found(self, client: TestClient):
        response = client.delete(f"{url}{invalid_uuid}")
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()["message"] == message_delete_error

    def test_delete_kibon_donjak(self, client: TestClient, kibon_donjak):
        response = client.post(url, json=kibon_donjak)
        assert response.status_code == HTTPStatus.OK
        response = client.delete(f"{url}{response.json()['id']}")
        assert response.status_code == HTTPStatus.OK
        assert response.json()["message"] == "Kibon Donjak deletado com sucesso."
