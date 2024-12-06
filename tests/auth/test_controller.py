from http import HTTPStatus

from starlette.testclient import TestClient

from tests.utils import get_authorization_headers_invalid, user_valid

url = '/auth'


class TestAuth:
    def test_login(self, client: TestClient):
        user = user_valid()
        response = client.post(url, json=user)
        assert response.status_code == HTTPStatus.OK

    def test_login_wrong_password(self, client: TestClient):
        user = user_valid()
        user['password'] = '<PASSWORD>'
        response = client.post(url, json=user)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()['message'] == 'Credenciais inválidas.'

    def test_logout(self, client: TestClient):
        user = user_valid()
        response = client.post(url, json=user)
        assert response.status_code == HTTPStatus.OK
        response = client.post(
            url + '/logout',
            headers={
                'Authorization': f"Bearer {response.json()['access_token']}"
            },
        )
        assert response.status_code == HTTPStatus.OK
        assert response.json()['message'] == 'Logout realizado com sucesso.'

    def test_logout_wrong_access_token(self, client: TestClient):
        data = get_authorization_headers_invalid(client)
        response = client.post(url + '/logout', headers=data)
        assert response.status_code == HTTPStatus.UNAUTHORIZED
        assert response.json()['detail'] == 'Not authenticated'
