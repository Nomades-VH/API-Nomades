from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from tests.utils import get_kick_by_id, invalid_uuid, kick_valid

message_get_error = 'Não foi possível encontrar esse chute.'
message_update_error = 'Não foi possível atualizar o chute.'
message_delete_error = 'Não foi possível deletar o chute.'

url = '/kick/'


class TestKick:
    @pytest.fixture(scope='function')
    def kick(self):
        return kick_valid()  # Retorna a variável kick

    def test_get_kicks_without_kicks(self, client: TestClient):
        response = client.get(url)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()['message'] == 'Não foram encontrados chutes.'

    def test_post_kick(self, client: TestClient, kick):
        response = client.post(url, json=kick)
        assert response.status_code == HTTPStatus.CREATED
        kick_created = get_kick_by_id(response.json()['id'], client)
        assert kick_created['name'] == kick['name']

    def test_get_kicks(self, client: TestClient, kick):
        client.post(url, json=kick)
        response = client.get(url)
        assert response.status_code == HTTPStatus.OK
        assert type(response.json()) == list
        assert len(response.json()) > 0
        assert response.json()[0]['name'] == kick['name']

    def test_post_kick_existing_name(self, client: TestClient, kick):
        client.post(url, json=kick)
        response = client.post(url, json=kick)
        assert response.status_code == HTTPStatus.CONFLICT
        assert response.json()['message'] == f"{kick['name']} já existe."

    def test_post_kick_with_wrong_name(self, client: TestClient, kick):
        kick['name'] = None
        response = client.post(url, json=kick)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert (
            response.json()['message']
            == 'Argumento inválido ou ausência de argumentos.: name'
        )

    def test_post_kick_with_wrong_meaning(self, client: TestClient, kick):
        kick['description'] = None
        response = client.post(url, json=kick)
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert (
            response.json()['message']
            == 'Argumento inválido ou ausência de argumentos.: description'
        )

    def test_post_band_without_arguments(self, client: TestClient):
        response = client.post(url, json={})
        assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
        assert (
            response.json()['message']
            == 'Argumento inválido ou ausência de argumentos.: name'
        )

    def test_get_by_id(self, client: TestClient, kick):
        client.post(url, json=kick)
        kick = client.get(url).json()[0]
        response = client.get(f'{url}{kick["id"]}')
        assert response.status_code == HTTPStatus.OK
        assert response.json() == kick

    def test_get_by_id_not_found(self, client: TestClient, kick):
        client.post(url, json=kick)
        response = client.get(f'{url}{invalid_uuid}')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()['message'] == message_get_error

    def test_update_band_not_found(self, client: TestClient, kick):
        response = client.put(f'{url}{invalid_uuid}', json=kick)
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert (
            response.json()['message']
            == message_update_error + ' ID não encontrado.'
        )

    def test_update_band(self, client: TestClient, kick):
        client.post(url, json=kick)
        kick_caught = client.get(url).json()[0]
        kick['name'] = 'new name'
        response = client.put(f"{url}{kick_caught['id']}", json=kick)
        assert response.status_code == HTTPStatus.OK
        new_kick_caught = client.get(f'{url}{kick_caught["id"]}')
        assert new_kick_caught.json()['name'] == kick['name']
        assert (
            new_kick_caught.json()['updated_at'] != kick_caught['updated_at']
        )

    def test_delete_kick_not_found(self, client: TestClient):
        response = client.delete(f'{url}{invalid_uuid}')
        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json()['message'] == message_delete_error + ' ID não encontrado.'

    def test_delete_kick(self, client: TestClient, kick):
        response = client.post(url, json=kick)
        assert response.status_code == HTTPStatus.CREATED
        response = client.delete(f"{url}{response.json()['id']}")
        assert response.status_code == HTTPStatus.NO_CONTENT
