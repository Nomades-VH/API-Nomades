from http import HTTPStatus
from unittest import TestCase, main
import requests
from app.band import services as sv
from app.band.models import Band as BandModel
from tests.utils import send_request


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
        r = send_request('http://127.0.0.1:8000/auth', requests.post, headers=self.headers, data={
                "username": "felipe-root",
                "password": "FelipePy"
            })
        self.headers.update({
            'Authorization': 'Bearer ' + r.json()['access_token']
        })

    def _get_band(self) -> dict:
        return requests.get(url=self.url, headers=self.headers).json()[0]

    def test_1_post_band(self):
        r = send_request(self.url, requests.post, headers=self.headers, data=self.band)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        r = send_request(self.url, requests.get, headers=self.headers)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertGreater(len(r.json()), 0)

    def test_2_post_band_with_wrong_gub(self):
        band = self.band.copy()
        band['gub'] = None
        r = send_request(self.url, requests.post, headers=self.headers, data=band)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo gub é necessário')

    def test_3_post_band_with_wrong_name(self):
        band = self.band.copy()
        band['name'] = None
        r = send_request(self.url, requests.post, headers=self.headers, data=band)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo name é necessário')

    def test_4_post_band_with_wrong_meaning(self):
        band = self.band.copy()
        band['meaning'] = None
        r = send_request(self.url, requests.post, headers=self.headers, data=band)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo meaning é necessário')

    # def test_5_post_band_without_arguments(self):
    #     r = self._send_request(requests.post, band={})
    #     self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)

    def test_5_post_band_with_a_gub_from_band_created(self):
        band = self.band.copy()
        r = send_request(self.url, requests.post, headers=self.headers, data=band)
        band = dict_to_model(band)
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(r.json()['message'], f'A faixa com o gub {band.gub} já existe.')

    def test_6_post_band_with_a_name_from_band_created(self):
        band = self.band.copy()
        band['gub'] = 1000
        r = send_request(self.url, requests.post, headers=self.headers, data=band)
        band = dict_to_model(band)
        self.assertEqual(r.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(r.json()['message'], f'Erro ao criar a faixa.: {band.name} já existe.')

    def test_7_get_bands(self):
        r = send_request(self.url, requests.get, headers=self.headers)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(type(r.json()), list)

    def test_8_get_by_id(self):
        band_id = self._get_band()['id']
        r = send_request(self.url, requests.get, headers=self.headers, url_increment=band_id)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(type(r.json()), dict)

    def test_9_get_by_gub(self):
        band = self._get_band()
        r = send_request(self.url, requests.get, headers=self.headers, url_increment=f"gub/{band['gub']}")
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(r.json()['gub'], band['gub'])

    def test_10_get_by_gub_not_found(self):
        band = self._get_band()
        r = send_request(self.url, requests.get, headers=self.headers, url_increment='gub/55')
        self.assertEqual(r.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(r.json()['message'], f'Faixa não encontrada.')

    def test_11_get_by_id_not_found(self):
        id = '8c3846d3-f05b-41ea-a580-d54fa2aa5a1b'
        r = send_request(self.url, requests.get, headers=self.headers, url_increment=id)
        self.assertEqual(r.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(r.json()['message'], f'Faixa não encontrada.')

    def test_12_update_band_not_found(self):
        band = self._get_band()
        r = send_request(self.url, requests.put, headers=self.headers, url_increment="551c3af5-f66f-4d8e-9413-43e995eb8ee1", data=band)
        self.assertEqual(r.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(r.json()['message'], f"Faixa não atualizada.")

    def test_13_update_band(self):
        band = self._get_band()
        band_model = dict_to_model(band)
        band_id = band['id']
        band_model.name = "Faixa Modificada"
        r = send_request(self.url, requests.put, headers=self.headers, url_increment=band_id, data=band)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        r = send_request(self.url, requests.get, headers=self.headers, url_increment=band_id)
        self.assertEqual(r.json()['name'], band['name'])

    def test_14_delete_band_not_found(self):
        band_id = self._get_band()['id']
        r = send_request(self.url, requests.delete, headers=self.headers, url_increment="551c3af5-f66f-4d8e-9413-43e995eb8ee1")
        self.assertEqual(r.status_code, HTTPStatus.NOT_FOUND)
        self.assertEqual(r.json()['message'], f'Faixa não encontrada.')
        r = send_request(self.url, requests.get, headers=self.headers, url_increment=band_id)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(type(r.json()), dict)

    def test_15_delete_band(self):
        band_id = self._get_band()['id']
        r = send_request(self.url, requests.delete, headers=self.headers, url_increment=band_id)
        self.assertEqual(r.status_code, HTTPStatus.OK)
        self.assertEqual(r.json()['message'], f'Faixa deletada.')


if __name__ == "__main__":
    main()
