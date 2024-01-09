import json
from http import HTTPStatus
from unittest import TestCase, main
import requests
from app.band import services as sv
from app.band.models import Band as BandModel


def dict_to_model(band: dict) -> BandModel:
    return BandModel(
        gub=band['gub'],
        name=band['name'],
        meaning=band['meaning']
    )


class TestController(TestCase):
    url: str = "http://127.0.0.1:8000/band/"
    band: dict = {
        "gub": 100,
        "name": "Faixa para os testes automatizados",
        "meaning": "Pureza/Inicio"
    }

    headers = {}
    sv = sv

    def test_0_get_authorization(self):
        r = self._send_request(requests.post, url='http://127.0.0.1:8000/auth', data={
                "username": "felipe-root",
                "password": "FelipePy"
            })

        self.headers.update({
            'Authorization': 'Bearer ' + r.json()['access_token']
        })

    def _get_band(self) -> dict:
        return requests.get(url=self.url, headers=self.headers).json()[0]

    def _send_request(self, func, url_increment='', url=None, data=None):
        if data:
            return func(url=url or self.url + url_increment, data=json.dumps(data), headers=self.headers)

        return func(url=url or self.url + url_increment, headers=self.headers)

    def test_1_post_band(self):
        r = self._send_request(requests.post, data=self.band)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        r = self._send_request(requests.get)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertGreater(len(r.json()), 0)

    def test_2_post_band_with_wrong_gub(self):
        band = self.band.copy()
        band['gub'] = None
        r = self._send_request(requests.post, data=band)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo gub é necessário')

    def test_3_post_band_with_wrong_name(self):
        band = self.band.copy()
        band['name'] = None
        r = self._send_request(requests.post, data=band)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo name é necessário')

    def test_4_post_band_with_wrong_meaning(self):
        band = self.band.copy()
        band['meaning'] = None
        r = self._send_request(requests.post, data=band)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo meaning é necessário')

    # def test_5_post_band_without_arguments(self):
    #     r = self._send_request(requests.post, band={})
    #     self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_5_post_band_with_a_gub_from_band_created(self):
        band = self.band.copy()
        r = self._send_request(requests.post, data=band)
        band = dict_to_model(band)
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(r.json()['message'], f'A faixa com o gub {band.gub} já existe.')

    def test_6_post_band_with_a_name_from_band_created(self):
        band = self.band.copy()
        band['gub'] = 1000
        r = self._send_request(requests.post, data=band)
        band = dict_to_model(band)
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(r.json()['message'], f'Erro ao criar a faixa.: {band.name} já existe.')

    def test_6_get_bands(self):
        r = self._send_request(requests.get)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(type(r.json()), list)

    def test_7_get_by_id(self):
        band_id = self._get_band()['id']
        r = self._send_request(requests.get, url_increment=band_id)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(type(r.json()), dict)

    def test_8_get_by_id_not_exists(self):
        id = '8c3846d3-f05b-41ea-a580-d54fa2aa5a1b'
        r = self._send_request(requests.get, url_increment=id)
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(r.json()['message'], f'Não foi possível buscar essa faixa. Identificador {id} não encontrado.')

    def test_8_update_band(self):
        band = self._get_band()
        band_model = dict_to_model(band)
        band_id = band['id']
        band_model.name = "Faixa Modificada"
        r = self._send_request(requests.put, url_increment=band_id, data=band)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        r = self._send_request(requests.get, url_increment=band_id)
        self.assertEqual(r.json()['name'], band['name'])

    def test_99_delete_band(self):
        band_id = self._get_band()['id']
        r = self._send_request(requests.delete, url_increment=band_id)
        self.assertEqual(r.status_code, HTTPStatus.OK)


if __name__ == "__main__":
    main()
