from unittest import TestCase, main
import requests


class TestController(TestCase):
    url: str = "http://127.0.0.1:8000/band/"
    band: dict = {
        "gub": 1,
        "meaning": "Primeira faixa",
        "name": "Faixa branca",
        "fk_theory": "73f35408-be7e-4a24-b93d-9942e74b8515"
    }

    def test_get_all(self):
        r = requests.get(url=self.url)
        self.assertEqual(r.status_code, 200)

    def test_get_band(self):
        url = self.url + "eccdbe24-f118-48e7-bc54-c99ba9126598/"
        r = requests.get(url=url)
        self.assertEqual(r.status_code, 200)

    def test_post_band(self):
        r = requests.post(url=self.url, data=self.band)
        self.assertEqual(r.status_code, 200)


if __name__ == '__main__':
    main()
