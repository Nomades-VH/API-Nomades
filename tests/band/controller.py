from functools import wraps
from http import HTTPStatus
from unittest import TestCase
import requests

from app.band.models import Band as BandModel
from tests.utils import send_request

band: dict = {
        "gub": 100,
        "name": "Faixa para os testes automatizados",
        "meaning": "Pureza/Inicio"
    }
url: str = "http://127.0.0.1:8000/band/"
headers = {}


def dict_to_model(band: dict) -> BandModel:
    return BandModel(
        gub=band['gub'],
        name=band['name'],
        meaning=band['meaning']
    )


def get_band() -> dict:
    return requests.get(url=url, headers=headers).json()[0]


def add_and_delete_band(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        send_request(url, requests.post, headers=headers, data=band)
        func(*args, **kwargs)
        send_request(url, requests.delete, headers=headers, url_increment=get_band()['id'])
    return wrapper


def get_authorization():
    r = send_request('http://127.0.0.1:8000/auth', requests.post, data={
            "username": "felipe-root",
            "password": "FelipePy"
        })
    headers.update({'Authorization': 'Bearer ' + r.json()['access_token']})


get_authorization()


class TestController(TestCase):
    def test_post_band(self):
        r = send_request(url, requests.post, headers=headers, data=band)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        r = send_request(url, requests.get, headers=headers)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertGreater(len(r.json()), 0)
        send_request(url, requests.delete, headers=headers, url_increment=get_band()['id'])

    @add_and_delete_band
    def test_post_band_with_exists(self):
        r = send_request(url, requests.post, headers=headers, data=band)
        band_copy = dict_to_model(band.copy())
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(r.json()['message'], f'A faixa com o gub {band_copy.gub} já existe.')
        send_request(url, requests.delete, headers=headers, data=get_band())

    def test_post_band_with_wrong_gub(self):
        band_copy = band.copy()
        band_copy['gub'] = None
        r = send_request(url, requests.post, headers=headers, data=band_copy)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo gub é necessário')

    def test_post_band_with_wrong_name(self):
        band_copy = band.copy()
        band_copy['name'] = None
        r = send_request(url, requests.post, headers=headers, data=band_copy)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo name é necessário')

    def test_post_band_with_wrong_meaning(self):
        band_copy = band.copy()
        band_copy['meaning'] = None
        r = send_request(url, requests.post, headers=headers, data=band_copy)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo meaning é necessário')

    def test_post_band_without_arguments(self):
        r = send_request(url, requests.post, headers=headers, data={})
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    @add_and_delete_band
    def test_post_band_with_a_name_from_band_created(self):
        band_copy = band.copy()
        band_copy['gub'] = 2
        r = send_request(url, requests.post, headers=headers, data=band_copy)
        band_copy = dict_to_model(band_copy)
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(r.json()['message'], f'Erro ao criar a faixa.: {band_copy.name} já existe.')

    @add_and_delete_band
    def test_get_bands(self):
        r = send_request(url, requests.get, headers=headers)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(type(r.json()), list)

    @add_and_delete_band
    def test_get_by_id(self):
        band_id = get_band()['id']
        r = send_request(url, requests.get, headers=headers, url_increment=band_id)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(type(r.json()), dict)

    @add_and_delete_band
    def test_get_by_gub(self):
        band_copy = get_band()
        r = send_request(url, requests.get, headers=headers, url_increment=f"gub/{band_copy['gub']}")
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(r.json()['gub'], band_copy['gub'])

    def test_get_by_gub_not_found(self):
        r = send_request(url, requests.get, headers=headers, url_increment='gub/55')
        self.assertEqual(r.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(r.json()['message'], f'Faixa não encontrada.')

    def test_get_by_id_not_found(self):
        id = '8c3846d3-f05b-41ea-a580-d54fa2aa5a1b'
        r = send_request(url, requests.get, headers=headers, url_increment=id)
        self.assertEqual(r.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(r.json()['message'], f'Faixa não encontrada.')

    def test_update_band_not_found(self):
        r = send_request(url, requests.put, headers=headers, url_increment='551c3af5-f66f-4d8e-9413-43e995eb8ee1', data=band)
        self.assertEqual(r.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(r.json()['message'], f"Faixa não atualizada.")

    @add_and_delete_band
    def test_update_band(self):
        band_copy = get_band()
        band_model = dict_to_model(band_copy)
        band_id = band_copy['id']
        band_model.name = "Faixa Modificada"
        r = send_request(url, requests.put, headers=headers, url_increment=band_id, data=band_copy)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        r = send_request(url, requests.get, headers=headers, url_increment=band_id)
        self.assertEqual(r.json()['name'], band_copy['name'])

    def test_delete_band_not_found(self):
        r = send_request(url, requests.delete, headers=headers, url_increment="551c3af5-f66f-4d8e-9413-43e995eb8ee1")
        self.assertEqual(r.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(r.json()['message'], f'Faixa não encontrada.')

    def test_delete_band(self):
        send_request(url, requests.post, headers=headers, data=band)
        band_id = get_band()['id']
        r = send_request(url, requests.delete, headers=headers, url_increment=band_id)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(r.json()['message'], f'Faixa deletada.')
