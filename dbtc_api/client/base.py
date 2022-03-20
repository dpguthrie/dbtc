# stdlib
import abc
import os


class _Client(abc.ABC):
    def __init__(
        self,
        *,
        api_key: str = None,
        service_token: str = None,
        host: str = None,
    ):
        self.api_key = api_key or os.getenv('DBT_CLOUD_API_KEY')
        self.service_token = service_token or os.getenv('DBT_CLOUD_SERVICE_TOKEN')
        self._host = host or os.getenv('DBT_CLOUD_HOST', self._default_domain)

    @property
    @abc.abstractmethod
    def _default_domain(self):
        ...

    @property
    @abc.abstractmethod
    def _path(self):
        ...

    @property
    @abc.abstractmethod
    def _header_property(self):
        ...

    @property
    def _base_url(self):
        return f'https://{self._host}{self._path}'

    @property
    def headers(self):
        return {'Authorization': f'Token {getattr(self, self._header_property)}'}

    def full_url(self, path: str = None):
        if path is not None:
            return f'{self._base_url}{path}'

        return self._base_url
