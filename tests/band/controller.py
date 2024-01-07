import json
import uuid
from http import HTTPStatus
from unittest import TestCase, main
import requests
from app.band import services as sv


class TestController(TestCase):
    url: str = "http://127.0.0.1:8000/band/"
    band: dict = {
        "gub": 100,
        "name": "Faixa Branca",
        "meaning": "Pureza/Inicio"
    }

    headers = {
        "Authorization":
            "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI0ZWY4NTViYS1iNzI1LTQ1NWUtOTEyMy1hYmU4YTA1ZWIzNjAiLCJleHAiOjE3MDQ2NzUxNjJ9.iZWes1GOaP71UDP2iVg54Rg2ipzgcaaw2KyoD1T3NMg"
    }
    sv = sv

    def get_band(self) -> dict:
        return requests.get(url=self.url, headers=self.headers).json()[0]

    def test_1_post_band(self):
        r = requests.post(url=self.url, data=json.dumps(self.band), headers=self.headers)
        self.assertEqual(r.status_code, 200)
        r = requests.get(url=self.url, headers=self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertGreater(len(r.json()), 0)

    def test_2_post_band_with_incorrect_data(self):
        band = self.band.copy()
        band['meaning'] = None
        r = requests.post(url=self.url, data=json.dumps(band), headers=self.headers)
        self.assertEqual(r.status_code, HTTPStatus.UNPROCESSABLE_ENTITY)
        self.assertEqual(r.json()['message'], 'O campo meaning é necessário')

    def test_2_get_bands(self):
        r = requests.get(url=self.url, headers=self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(type(r.json()), list)
        self.assertEqual(type(r.json()[0]), dict)

    def test_3_get_by_id(self):
        band_id = self.get_band()['id']
        r = requests.get(url=self.url + band_id, headers=self.headers)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(type(r.json()), dict)

    def test_4_update_band(self):
        band = self.get_band()
        band.pop('created_for')
        band.pop('updated_for')
        band.pop('created_at')
        band.pop('updated_at')
        band.pop('fk_theory')
        band['name'] = "Faixa Modificada"
        r = requests.put(url=self.url + band['id'], data=json.dumps(band), headers=self.headers)
        self.assertEqual(r.status_code, 200)
        r = requests.get(url=self.url + band['id'], headers=self.headers)
        self.assertEqual(r.json()['name'], band['name'])

    def test_99_delete_band(self):
        band_id = self.get_band()['id']
        r = requests.delete(url=self.url+f'{band_id}', headers=self.headers)
        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    main()
