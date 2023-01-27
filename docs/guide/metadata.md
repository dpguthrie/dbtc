# Metadata

The `metadata` property on the `dbtCloudClient` class contains methods that allow a user to retrieve metadata which pertains to the accuracy, recency, configuration, and structure of the views and tables in the warehouse.

The Metadata API is a GraphQL API.  Normally, this would require a user to write a GraphQL query as part of the required payload.  However, this package provides a convenient interface that allows a user to write the GraphQL query in a more pythonic way.  There are two options:

1. Simply provide the minimal set of arguments to the functions below and get every field in the desired schema, including those that are nested.  An example is below for the `models` schema:

  ```python
  from dbtc import dbtCloudClient

  # Assuming DBT_CLOUD_SERVICE_TOKEN is set as an environment variable
  client = dbtCloudClient()
  job_id = 1

  models = client.metadata.get_models(job_id)
  ```

2. If you don't want or need all of the fields from a particular schema, use the optional `fields` argument to limit the amount of data that's returned.  This argument accepts a list of strings where the strings are names of fields within the schema.  Additionally, you can ask for nested fields using dot notation.

```python
from dbtc import dbtCloudClient

# Assuming DBT_CLOUD_SERVICE_TOKEN is set as an environment variable
client = dbtCloudClient()
job_id = 1

fields = [
    'uniqueId',
    'runId',
    'projectId',
    'environmentId',
    'alias',
    'description',
    'parentsSources.name',
    'parentsSources.criteria.warnAfter.period',
    'parentsSources.criteria.warnAfter.count',
]

models = client.metadata.get_models(job_id, fields=fields)
```

The video below provides some more detail.

<div style="position: relative; padding-bottom: 57.93991416309014%; height: 0;"><iframe src="https://www.loom.com/embed/5be093114c1d4e02a1bcc27c5976a4b2" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## get_exposure
::: dbtc.client.metadata._MetadataClient.get_exposure

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_exposure(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-exposure --job-id=12345
    ```

## get_exposures
::: dbtc.client.metadata._MetadataClient.get_exposures

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_exposures(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-exposures --job-id=12345
    ```

## get_macro
::: dbtc.client.metadata._MetadataClient.get_macro

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_macro(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-macro --job-id=12345
    ```

## get_macros
::: dbtc.client.metadata._MetadataClient.get_macros

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_macros(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-macros --job-id=12345
    ```

## get_metric
::: dbtc.client.metadata._MetadataClient.get_metric

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_metric(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-metric --job-id=12345
    ```

## get_metrics
::: dbtc.client.metadata._MetadataClient.get_metrics

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_metrics(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-metrics --job-id=12345
    ```

## get_model
::: dbtc.client.metadata._MetadataClient.get_model

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_model(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-model --job-id=12345
    ```

## get_model_by_environment
::: dbtc.client.metadata._MetadataClient.get_model_by_environment

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_model_by_environment(
        environment_id, unique_id
    )
    ```

=== "CLI"

    ```bash
    dbtc get-model-by-environment --environment-id=12345 --unique-id=models.tpch.order_items
    ```

## get_models
::: dbtc.client.metadata._MetadataClient.get_models

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_models(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-models --job-id=12345
    ```

## get_seed
::: dbtc.client.metadata._MetadataClient.get_seed

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_seed(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-seed --job-id=12345
    ```

## get_seeds
::: dbtc.client.metadata._MetadataClient.get_seeds

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_seeds(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-seeds --job-id=12345
    ```

## get_snapshot
::: dbtc.client.metadata._MetadataClient.get_snapshot

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_snapshot(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-snapshot --job-id=12345
    ```

## get_snapshots
::: dbtc.client.metadata._MetadataClient.get_snapshots

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_snapshots(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-snapshots --job-id=12345
    ```

## get_source
::: dbtc.client.metadata._MetadataClient.get_source

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_source(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-source --job-id=12345
    ```

## get_sources
::: dbtc.client.metadata._MetadataClient.get_sources

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_sources(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-sources --job-id=12345
    ```

## get_test
::: dbtc.client.metadata._MetadataClient.get_test

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_test(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-test --job-id=12345
    ```

## get_tests
::: dbtc.client.metadata._MetadataClient.get_tests

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.get_tests(job_id)
    ```

=== "CLI"

    ```bash
    dbtc get-tests --job-id=12345
    ```

## query
::: dbtc.client.metadata._MetadataClient.query

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py

    query = '{models(jobId: 1) {uniqueId}}'

    client.metadata.query(query)
    ```
