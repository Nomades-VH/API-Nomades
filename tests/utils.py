import os

from fastapi.testclient import TestClient

email_root = os.environ.get("ROOT_USER_EMAIL")
password_root = os.environ.get("ROOT_USER_PASSWORD")
invalid_uuid = "f7f00446-6d6a-417c-82e5-33a0698af17b"


def get_authorization(client: TestClient):
    data = {"email": email_root, "password": password_root}

    token = client.post("/auth", json=data)
    return {"Authorization": "Bearer " + token.json()["access_token"]}


def get_authorization_headers_invalid(client: TestClient):
    data = get_authorization(client)
    data["Authorization"] = data["Authorization"][7:]
    return data


def get_user_info(client: TestClient):
    return client.get("/user/", headers=get_authorization(client)).json()[0]


def user_valid() -> dict:
    return {"email": email_root, "password": password_root}


def band_valid() -> dict:
    return {
        "gub": 1,
        "name": "string",
        "meaning": "string",
        "theory": "string",
        "breakdown": "string",
        "stretching": "string",
    }


def poomsae_valid() -> dict:
    return {"name": "Saju Ap Tchagui", "description": "Ri (CALOR E BRILHO)"}

def kick_valid() -> dict:
    return {"name": "Bandal Tchagui", "description": "Chute lateral na linha de cintura"}

def kibon_donjak_valid() -> dict:
    return {"name": "Ap Kubi Are Makgi", "description": "Defesa baixo"}
  

def band_invalid() -> dict:
    return {
        "gub": "string",
        "name": "string",
        "meaning": "string",
        "theory": "string",
        "breakdown": "string",
        "stretching": "string",
    }


def get_band_by_gub(gub: int, client: TestClient) -> dict:
    return client.get(url=f"/band/gub/{gub}").json()

def get_kick_by_id(id: str, client: TestClient) -> dict:
    return client.get(url=f"/kick/{id}").json()

def get_poomsae_by_id(id: str, client: TestClient) -> dict:
    return client.get(url=f"/poomsae/{id}").json()

def get_kibon_donjak_by_id(id: str, client: TestClient) -> dict:
    return client.get(url=f"/kibon_donjak/{id}").json()
  