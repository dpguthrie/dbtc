# first party
from dbtc.client.cloud import _CloudClient
from dbtc.client.metadata import _MetadataClient


class dbtCloudClient:
    def __init__(self, **kwargs):
        self.cloud = _CloudClient(**kwargs)
        self.metadata = _MetadataClient(**kwargs)
