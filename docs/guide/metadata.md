# Metadata

The `metadata` property on the `dbtCloudClient` class contains methods that allow a user to retrieve metadata which pertains to the accuracy, recency, configuration, and structure of the views and tables in the warehouse.


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
