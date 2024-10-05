# third party
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# first party
from dbtc.client.admin import _AdminClient
from dbtc.client.metadata import _MetadataClient
from dbtc.client.semantic_layer import _SemanticLayerClient


class dbtCloudClient:
    def __init__(self, **kwargs):
        try:
            retry = Retry(
                total=5,
                backoff_factor=2,
                status_forcelist=[429, 500, 502, 503, 504],
            )
            adapter = HTTPAdapter(max_retries=retry)
            session = requests.Session()
            session.mount("https://", adapter)
        except Exception as e:
            raise e
        self.cloud = _AdminClient(session, **kwargs)
        self.metadata = _MetadataClient(session, **kwargs)
        self.sl = _SemanticLayerClient(session, **kwargs)
