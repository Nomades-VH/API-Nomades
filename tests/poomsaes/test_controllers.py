from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.utils import poomsae_valid, get_poomsae_by_id, invalid_uuid

message_get_error = "Não foi encontrado o poomsae."
message_update_error = "Não foi possível atualizar o Poomsae."
message_delete_error = "Não foi possível deletar o poomsae."

url = "/poomsae/"


class TestPoomsae:

    @pytest.fixture
    def poomsae(self):
        return poomsae_valid()  # Retorna a variável poomsae

    class TestGet:
        def test_get_poomsaes_without_poomsaes(self, client: TestClient):
            response = client.get(url)
            assert response.status_code == HTTPStatus.NOT_FOUND
            assert response.json()["message"] == "Não foram encontrados poomsaes."

        def test_post_poomsae(self, client: TestClient, poomsae):
            response = client.post(url, json=poomsae)
            assert response.status_code == HTTPStatus.OK
            poomsae_created = get_poomsae_by_id(response.json()["id"], client)
            assert poomsae_created["name"] == poomsae["name"]

        def test_get_poomsaes(self, client: TestClient, poomsae):
            client.post(url, json=poomsae)
            response = client.get(url)
            assert response.status_code == HTTPStatus.OK
            assert type(response.json()) == list
            assert len(response.json()) > 0
            assert response.json()[0]["name"] == poomsae["name"]

    class TestPost:
        def test_post_poomsae_existing_name(self, client: TestClient, poomsae):
            client.post(url, json=poomsae)
            response = client.post(url, json=poomsae)
            assert response.status_code == HTTPStatus.BAD_REQUEST
            assert response.json()["message"] == f"{poomsae['name']} já existe."

        def test_post_poomsae_with_wrong_name(self, client: TestClient, poomsae):
            poomsae["name"] = None
            response = client.post(url, json=poomsae)
            assert response.status_code == HTTPStatus.BAD_REQUEST
            assert (
                response.json()["message"]
                == "Argumento inválido ou ausência de argumentos.: name"
            )

        def test_post_poomsae_with_wrong_meaning(self, client: TestClient, poomsae):
            poomsae["description"] = None
            response = client.post(url, json=poomsae)
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

    class TestGetById:
        def test_get_by_id(self, client: TestClient, poomsae):
            client.post(url, json=poomsae)
            poomsae = client.get(url).json()[0]
            response = client.get(f'{url}{poomsae["id"]}')
            assert response.status_code == HTTPStatus.OK
            assert response.json() == poomsae

        def test_get_by_id_not_found(self, client: TestClient, poomsae):
            client.post(url, json=poomsae)
            response = client.get(f"{url}{invalid_uuid}")
            assert response.status_code == HTTPStatus.NOT_FOUND
            assert response.json()["message"] == message_get_error

    class TestUpdate:
        def test_update_band_not_found(self, client: TestClient, poomsae):
            response = client.put(f"{url}{invalid_uuid}", json=poomsae)
            assert response.status_code == HTTPStatus.NOT_FOUND
            assert (
                response.json()["message"]
                == message_update_error + " ID não encontrado."
            )

        def test_update_band(self, client: TestClient, poomsae):
            client.post(url, json=poomsae)
            poomsae_caught = client.get(url).json()[0]
            poomsae["name"] = "new name"
            response = client.put(f"{url}{poomsae_caught['id']}", json=poomsae)
            assert response.status_code == HTTPStatus.OK
            new_poomsae_caught = client.get(f'{url}{poomsae_caught["id"]}')
            assert new_poomsae_caught.json()["name"] == poomsae["name"]
            assert (
                new_poomsae_caught.json()["updated_at"] != poomsae_caught["updated_at"]
            )

    class TestDelete:
        def test_delete_poomsae_not_found(self, client: TestClient):
            response = client.delete(f"{url}{invalid_uuid}")
            assert response.status_code == HTTPStatus.NOT_FOUND
            assert response.json()["message"] == message_delete_error

        def test_delete_poomsae(self, client: TestClient, poomsae):
            response = client.post(url, json=poomsae)
            assert response.status_code == HTTPStatus.OK
            response = client.delete(f"{url}{response.json()['id']}")
            assert response.status_code == HTTPStatus.OK
            response = client.get(url)
            assert response.status_code == HTTPStatus.NOT_FOUND
