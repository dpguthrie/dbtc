# stdlib
import os

# third party
import pytest

# first party
from dbtc import dbtCloudClient


@pytest.fixture(scope="session")
def dbtc_client():
    return dbtCloudClient(
        service_token=os.getenv("DBT_CLOUD_SERVICE_TOKEN"),
        api_key=os.getenv("DBT_CLOUD_API_KEY"),
        environment_id=218762,
    )
