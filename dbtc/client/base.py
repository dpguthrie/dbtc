# stdlib
import abc
import inspect
import os
import uuid
from typing import Callable, Optional

# third party
import rudder_analytics

# first party
from dbtc import __version__
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
        self.api_key: Optional[str] = api_key or os.getenv('DBT_CLOUD_API_KEY', None)
        self.service_token: Optional[str] = service_token or os.getenv(
            'DBT_CLOUD_SERVICE_TOKEN', None
        )
        self._host: Optional[str] = host or os.getenv(
            'DBT_CLOUD_HOST', self.DEFAULT_DOMAIN
        )
        self.do_not_track: bool = do_not_track
        self._anonymous_id: str = str(uuid.uuid4())
        self._called_from: Optional[str] = None
        self.console = err_console

    DEFAULT_DOMAIN = 'cloud.getdbt.com'

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

    def _send_track(self, event_name: str, func: Callable, *args, **kwargs):
        func_args = [a for a in inspect.getfullargspec(func).args if a != 'self']
        properties = {
            'method': func.__name__,
            'dbtc_version': __version__,
            'called_from': self._called_from,
            **dict(zip(func_args, args)),
            **kwargs,
        }
        properties = {k: v for k, v in properties.items() if not k.endswith('_id')}
        rudder_analytics.track(self._anonymous_id, event_name, properties)
