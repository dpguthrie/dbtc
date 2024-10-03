# stdlib
import abc
import os
from typing import Optional

# third party
import requests

# first party
from dbtc.console import err_console


class _Client(abc.ABC):
    def __init__(
        self,
        session: requests.Session,
        *,
        api_key: str = None,
        service_token: str = None,
        host: str = None,
        environment_id: int = None,
        use_beta_endpoint: bool = True,
    ):
        self.api_key: Optional[str] = api_key or os.getenv("DBT_CLOUD_API_KEY", None)
        self.service_token: Optional[str] = service_token or os.getenv(
            "DBT_CLOUD_SERVICE_TOKEN", None
        )
        self._host: Optional[str] = host or os.getenv(
            "DBT_CLOUD_HOST", self.DEFAULT_DOMAIN
        )
        self.environment_id = environment_id or os.getenv(
            "DBT_CLOUD_ENVIRONMENT_ID", None
        )
        self._use_beta = use_beta_endpoint
        self.console = err_console
        self.session = session
        self.session.headers = self.headers

    DEFAULT_DOMAIN = "cloud.getdbt.com"

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
        return f"https://{self._host}{self._path}"

    @property
    def headers(self):
        return {
            "Authorization": f"Bearer {getattr(self, self._header_property)}",
            "Content-Type": "application/json",
        }

    def full_url(self, path: str = None):
        if path is not None:
            return f"{self._base_url}{path}"

        return self._base_url
