# stdlib
import abc
import os


class _Client(abc.ABC):
    def __init__(
        self,
        *,
        api_key: str = None,
        service_token: str = None,
    ):
        self.api_key = api_key or os.getenv('DBT_CLOUD_API_KEY')
        self.service_token = service_token or os.getenv('DBT_CLOUD_SERVICE_TOKEN')

    @property
    @abc.abstractmethod
    def _header_property(self):
        ...

    @property
    @abc.abstractmethod
    def _base_url(self):
        ...

    @property
    def headers(self):
        return {'Authorization': f'Token {getattr(self, self._header_property)}'}

    def full_url(self, path: str = None):
        if path is not None:
            return f'{self._base_url}{path}'

        return self._base_url
