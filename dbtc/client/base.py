# stdlib
import abc
import os
import uuid

# third party
import rudder_analytics

# first party
from dbtc.console import err_console

rudder_analytics.write_key = "2KbeK4vnN03rxKRcL8YNIDvk1pz"
rudder_analytics.data_plane_url = "https://dbtlabsdonqtb.dataplane.rudderstack.com"


class _Client(abc.ABC):
    def __init__(
        self,
        *,
        api_key: str = None,
        service_token: str = None,
        host: str = None,
        do_not_track: bool = False,
    ):
        self.api_key = api_key or os.getenv('DBT_CLOUD_API_KEY', None)
        self.service_token = service_token or os.getenv('DBT_CLOUD_SERVICE_TOKEN', None)
        self._host = host or os.getenv('DBT_CLOUD_HOST', self._default_domain)
        self.console = err_console
        self.do_not_track = do_not_track
        self._anonymous_id = str(uuid.uuid4())
        self._track = rudder_analytics.track

    @property
    @abc.abstractmethod
    def _default_domain(self):
        """Default used when host is not provided by a user"""

    @property
    @abc.abstractmethod
    def _path(self):
        """Path where specific resource is located"""

    @property
    @abc.abstractmethod
    def _header_property(self):
        """Define what property to use within the headers passed with a request"""

    @property
    def _base_url(self):
        return f'https://{self._host}{self._path}'

    @property
    def headers(self):
        return {
            'Authorization': f'Token {getattr(self, self._header_property)}',
            'Content-Type': 'application/json',
        }

    def full_url(self, path: str = None):
        if path is not None:
            return f'{self._base_url}{path}'

        return self._base_url
