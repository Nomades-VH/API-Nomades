import json

import requests


def send_request(url: str, func: requests, *, headers=None, url_increment='', data=None):
    if data:
        return func(url=url + url_increment, data=json.dumps(data), headers=headers)

    return func(url=url + url_increment, headers=headers)
