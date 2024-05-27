# Semantic Layer

The dbt Cloud Semantic Layer is used as an intermediary between your data platform and the various consumption points you have within your organization.  Metricflow, the underlying piece of technology within the Semantic Layer, is responsible for translating the request from a client application into SQL that the underlying data platform understands.  What this means for you?  Define your metrics in a single place - within your dbt project - and leverage that definition across your stack to enable any stakeholder, regardless of technical capability or preferred medium.

This client has a convenient wrapper around the [Semantic Layer GraphQL API](https://docs.getdbt.com/docs/dbt-cloud-apis/sl-graphql) and enables those that are using python to consume that governed set of metrics defined in your dbt project.

If you're unfamiliar either with the Schema to query metrics defined in your project or even how to write a GraphQL query, I highly recommend going to the [Semantic Layer GraphQL API playground](https://semantic-layer.cloud.getdbt.com/api/graphql).  You'll be able to interactively explore the Schema while watching it write a GraphQL query for you!

## Usage

The `sl` property on the `dbtCloudClient` class contains the methods that allow for interaction with dbt Cloud's Semantic Layer.  The one requirement when initializing the class is to pass the environment ID that you've configured within dbt Cloud.  For example

```python
from dbtc import dbtCloudClient

# Assuming I have `DBT_CLOUD_SERVICE_TOKEN` as an env var
client = dbtCloudClient(environment_id=1)
```

Additionally, you'll want to be sure that you pass the appropriate host when initializing the class.  As a default, the host mapped to the North America region will be used.  More regions and their corresonding host values (see Access URL) can be found [here](https://docs.getdbt.com/docs/cloud/about-cloud/access-regions-ip-addresses)

```python
from dbtc import dbtCloudClient

# Assuming I have `DBT_CLOUD_SERVICE_TOKEN` as an env var
client = dbtCloudClient(environment_id=1, host="emea.dbt.com")
```

## list_dimensions
::: dbtc.client.semantic_layer._SemanticLayerClient.list_dimensions

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.sl.list_dimensions(metrics=["total_revenue", "total_profit"])
    ```

## list_entities
::: dbtc.client.semantic_layer._SemanticLayerClient.list_entities

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.sl.list_entities(metrics=["total_revenue", "total_profit"])
    ```

## list_measures
::: dbtc.client.semantic_layer._SemanticLayerClient.list_measures

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.sl.list_measures(metrics=["total_revenue", "total_profit"])
    ```

## list_metrics
::: dbtc.client.semantic_layer._SemanticLayerClient.list_metrics

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.sl.list_metrics()
    ```

## list_metrics_for_dimensions
::: dbtc.client.semantic_layer._SemanticLayerClient.list_metrics_for_dimensions

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.sl.list_metrics_for_dimensions(
        dimensions=["customer__region", {"name": "metric_time": "grain": "day"}]
    )
    ```

## list_queryable_granularities
::: dbtc.client.semantic_layer._SemanticLayerClient.list_queryable_granularities

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.sl.list_queryable_granularities(metrics=["total_revenue"])
    ```

## list_saved_queries
::: dbtc.client.semantic_layer._SemanticLayerClient.list_saved_queries

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.sl.list_saved_queries()
    ```

## list_dimension_values
::: dbtc.client.semantic_layer._SemanticLayerClient.list_dimension_values

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.sl.list_dimension_values(
        group_by=["customer__region"],
        output_format="list",
    )
    ```

## query
::: dbtc.client.semantic_layer._SemanticLayerClient.query

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    query_result = client.sl.query(
        metrics=["total_revenue", "total_profit"],
        group_by=["customer__region"],
    )

    # query_result is an instance of QueryResult, data is in the `result` attribute
    query_result.result # default will be a pandas.DataFrame

    # Also view the generated SQL
    query_result.sql

    # And the query_id
    query_result.query_id

    # Or do something with the status
    if query_result.status == "SUCCESSFUL":
        ...

    ```