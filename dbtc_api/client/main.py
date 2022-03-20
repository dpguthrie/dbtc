# first party
from dbtc_api.client.cloud import _CloudClientV2
from dbtc_api.client.metadata import _MetadataClient


class dbtCloudClient:
    def __init__(self, **kwargs):
        self.cloud = _CloudClientV2(**kwargs)
        self.metadata = _MetadataClient(**kwargs)
