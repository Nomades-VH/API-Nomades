from unittest import TestCase, main
import requests


class TestTheoryController(TestCase):
    url: str = "http://127.0.0.1:8000/theory/"
    theory = {"description": "Conhecimentos básicos sobre o Taekwondo"}

    def test_add_theory(self):
        r = requests.post(url=self.url, json=self.theory)
        self.assertEqual(r.status_code, 200)

    # TODO: Não está implementado corretamente (Sempre retornará código 200)
    def test_get_theories(self):
        r = requests.get(url=self.url)
        self.assertEqual(r.status_code, 200)


if __name__ == "__main__":
    main()
