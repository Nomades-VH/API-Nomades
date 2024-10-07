import os

from fastapi.testclient import TestClient

email = os.environ.get("ROOT_USER_EMAIL")
password = os.environ.get("ROOT_USER_PASSWORD")


def get_authorization_headers(client: TestClient):
    data = {
        "email": email,
        "password": password
    }

    token = client.post('/auth', json=data)
    return {'Authorization': 'Bearer ' + token.json()['access_token']}


def get_authorization_headers_invalid(client: TestClient):
    data = get_authorization_headers(client)
    data['Authorization'] = data['Authorization'][7:]
    return data


def get_user_info(client: TestClient):
    return client.get('/user/', headers=get_authorization_headers(client)).json()[0]


def user_valid() -> dict:
    return {
        "email": email,
        "password": password
    }


def band_valid() -> dict:
    return {
        "gub": 1,
        "name": "string",
        "meaning": "string",
        "theory": "string",
        "breakdown": "string",
        "stretching": "string"
    }

def poomsae_valid() -> dict:
    return {
        "name": "Saju Ap Tchagui",
        "description": "Ri (CALOR E BRILHO)"
    }


def band_invalid() -> dict:
    return {
        "gub": "string",
        "name": "string",
        "meaning": "string",
        "theory": "string",
        "breakdown": "string",
        "stretching": "string"
    }


def get_band_by_gub(gub: int, auth, client: TestClient) -> dict:
    return client.get(url=f"/band/gub/{gub}", headers=auth).json()
