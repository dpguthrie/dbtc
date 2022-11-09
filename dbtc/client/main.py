# first party
from dbtc.client.admin import _AdminClient
from dbtc.client.metadata import _MetadataClient


class dbtCloudClient:
    def __init__(self, **kwargs):
        self.cloud = _AdminClient(**kwargs)
        self.metadata = _MetadataClient(**kwargs)
