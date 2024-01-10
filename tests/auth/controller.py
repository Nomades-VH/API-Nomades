import json
from http import HTTPStatus
from unittest import TestCase, main
import requests
from app.auth import services as sv
from app.auth.entities import Auth
from tests.utils import send_request


class TestController(TestCase):
    url: str = "http://127.0.0.1:8000/auth/"
    headers = {}
    sv = sv

    def test_0_login(self):
        r = send_request(self.url, self.headers)

if __name__ == "__main__":
    main()
