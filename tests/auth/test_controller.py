from http import HTTPStatus

from starlette.testclient import TestClient

from tests.utils import user_valid, get_authorization_headers

url = "/auth"


def test_login(client: TestClient):
    user = user_valid()
    response = client.post(url, json=user)
    assert response.status_code == HTTPStatus.OK


def test_login_wrong_password(client: TestClient):
    user = user_valid()
    user["password"] = "<PASSWORD>"
    response = client.post(url, json=user)
    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()["message"] == 'Credenciais inválidas.'
