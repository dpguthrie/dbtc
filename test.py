# first party
from dbtc import dbtCloudClient

client = dbtCloudClient(
    service_token='dbts_CqVWegELUCA3L3kj4Ydu68a2_ZqPcgdPbMExfe8QECR-yW7i6oejM3aQ==',
    host='emea.dbt.com',
)

client.cloud.list_accounts()
