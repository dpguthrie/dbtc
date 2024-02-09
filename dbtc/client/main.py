# third party
import requests

# first party
from dbtc.client.admin import _AdminClient
from dbtc.client.metadata import _MetadataClient
from dbtc.client.semantic_layer import _SemanticLayerClient


class dbtCloudClient:
    def __init__(self, **kwargs):
        session = requests.Session()
        self.cloud = _AdminClient(session, **kwargs)
        self.metadata = _MetadataClient(session, **kwargs)
        self.sl = _SemanticLayerClient(session, **kwargs)
