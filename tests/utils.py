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


def get_authorization_headers_invalid(client: TestClient):
    data = get_authorization_headers(client)
    data['Authorization'] = data['Authorization'][7:]
    print(data)
    return data


def get_user_info(client: TestClient):
    return client.get('/user/', headers=get_authorization_headers(client)).json()[0]


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
        "meaning": "string",
        "theory": "string",
        "breakdown": "string",
        "stretching": "string"
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
