# Introduction

## Python

### Class

The `dbtCloudClient` class is the main interface through which you will interact with dbt Cloud API endpoints.  The class accepts three optional arguments:

- `api_key`
- `service_token`
- `host`

An `api_key` can be used to access endpoints from any version of the dbt Cloud API (v2 or v3).  The `service_token` can be used for *either* the dbt Cloud API or the Metadata API.  If you have the proper [permissions](https://docs.getdbt.com/docs/dbt-cloud/dbt-cloud-api/service-tokens#permissions-for-service-account-tokens), you would only need to pass a service token.

```python
from dbtc import dbtCloudClient

client = dbtCloudClient(service_token='this-is-my-service-token')
```

Alternatively, you can set the following environment variables in place of passing the arguments to the class:

- `api_key` --> `DBT_CLOUD_API_KEY`
- `service_token` --> `DBT_CLOUD_SERVICE_TOKEN`
- `host` --> `DBT_CLOUD_HOST`

If you have set environment variables, and have the proper permissions, you'll be able to instantiate the `dbtCloudClient` class as follows:

```python
from dbtc import dbtCloudClient

client = dbtCloudClient()
```

!!! info
    The `host` argument is only necessary for customers on single-tenant instances

### Interfaces

The `dbtCloudClient` class contains two properties:

- `cloud` - instance of the `_AdminClient` class, which contains methods to create, read, update, and delete dbt Cloud resources
- `metadata` - instance of the `_MetadataClient` class, which contains methods to retrieve metadata generated from a dbt Cloud job run

**`cloud`**

```python
from dbtc import dbtCloudClient

# Assuming we've set the `DBT_CLOUD_SERVICET_TOKEN` environment variable`
client = dbtCloudClient()

accounts = client.cloud.list_accounts()
```

**`metadata`**

```python
from dbtc import dbtCloudClient

client = dbtCloudClient()

job_id = <xxx>
run_id = <xxx>
models = client.metadata.get_models(job_id, run_id)
```

## CLI

This package also comes with a command-line utility, `dbtc`.  All of the methods available through the `cloud` or `metadata` properties on the `dbtCloudClient` class are available through the command line as well.

The command line interface also accepts additional environment variables:

- `DBT_CLOUD_ACCOUNT_ID`
- `DBT_CLOUD_PROJECT_ID`

Setting these will reduce the amount of arguments you'll need to pass.

```bash
dbtc get-project --account-id=1 --project-id=1
```

Or, if you've set the `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID` environment variables.

```bash
dbtc get-project
```
