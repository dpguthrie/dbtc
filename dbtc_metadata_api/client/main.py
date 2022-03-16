# first party
from dbtc_metadata_api.client.cloud import _CloudClientV2
from dbtc_metadata_api.client.metadata import _MetadataClient


class dbtCloudClient:
    def __init__(self, **kwargs):
        self.cloud = _CloudClientV2(api_key=kwargs.get('api_key', None))
        self.metadata = _MetadataClient(service_token=kwargs.get('service_token', None))
