import os

from fastapi.testclient import TestClient

username = os.environ.get("ROOT_USER")
password = os.environ.get("ROOT_USER_PASSWORD")


def get_authorization_headers(client: TestClient):
    data = {
        "username": username,
        "password": password
    }
    token = client.post('/auth', json=data)
    return {'Authorization': 'Bearer ' + token.json()['access_token']}


def user_valid() -> dict:
    username = os.environ.get("ROOT_USER")
    password = os.environ.get("ROOT_USER_PASSWORD")
    return {
        "username": username,
        "password": password
    }


def band_valid() -> dict:
    return {
        "gub": 1,
        "name": "string",
        "meaning": "string"
    }


def band_invalid() -> dict:
    return {
        "gub": "string",
        "name": "string",
        "meaning": "string"
    }


def get_band_by_gub(gub: int, auth, client: TestClient) -> dict:
    return client.get(url=f"/band/gub/{gub}", headers=auth).json()
