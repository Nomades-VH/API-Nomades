import unittest

import requests

from tests.utils import send_request

url = "http://127.0.0.1:8000/auth"


class TestController(unittest.TestCase):

    def test_post_auth(self):
        r = send_request(url, requests.post, data={
            "username": "felipe-root",
            "password": "FelipePy"
        })
        self.assertEqual(r.status_code, 200)
