# stdlib
from typing import Dict

# third party
import requests

# first party
from dbtc_api.client.base import _Client


class _CloudClient(_Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.session.headers = self.headers

    _header_property = 'api_key'

    def _make_request(self, path: str, *, method: str = 'get', **kwargs) -> Dict:
        full_url = self.full_url(path)
        response = self.session.request(method, full_url, **kwargs)
        return response.json()
