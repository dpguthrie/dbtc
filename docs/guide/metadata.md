# Metadata

Every time dbt Cloud runs a project, it generates and stores information about the project. The metadata includes details about your project’s models, sources, and other nodes along with their execution results. With the dbt Cloud Discovery API, you can query this comprehensive information to gain a better understanding of your DAG and the data it produces.

By leveraging the metadata in dbt Cloud, you can create systems for data monitoring and alerting, lineage exploration, and automated reporting. This can help you improve data discovery, data quality, and pipeline operations within your organization.

The `metadata` property on the `dbtCloudClient` class contains a single method, `query`, that allows a user to interact with the [Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api).

If you're unfamiliar either with the Schema to query or even how to write a GraphQL query, I highly recommend going to the [dbt Cloud Discovery API playground](https://metadata.cloud.getdbt.com/beta/graphql). You'll be able to interactively explore the Schema while watching it write a GraphQL query for you!

## Usage

The `metadata` property on the `dbtCloudClient` class has a single method to pass a `query` string and `variables` that will be submitted in the payload with the `query`. It's important to note that as a default this package will use the beta endpoint at `https://metadata.cloud.getdbt.com/beta/graphql` (or your particular host). As of this writing, there are many more beta fields that allow for a user to retrieve performance, lineage, recommendations, and much more! If you don't want to use the beta endpoint, construct your `dbtCloudClient` as follows:

!!! warning
If you do end up not using the beta endpoint, only the `query` method will work properly.

```python
from dbtc import dbtCloudClient

# Assuming I have `DBT_CLOUD_SERVICE_TOKEN` as an env var
client = dbtCloudClient(use_beta_endpoint=False)

# Now all calls to the metadata service will use https://metadata.<host>.com/graphql
client.metadata.query(...)

```

## column_lineage

::: dbtc.client.metadata.\_MetadataClient.column_lineage

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.column_lineage(environment_id, "model.tpch.dim_customers")
    ```

=== "CLI"

    ```bash
    dbtc metadata column-lineage --environment-id 1 --unique-id "model.tpch.dim_customers"
    ```

## longest_executed_models

::: dbtc.client.metadata.\_MetadataClient.longest_executed_models

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.longest_executed_models(environment_id, "2024-01-23", "2024-01-24")
    ```

=== "CLI"

    ```bash
    dbtc metadata longest-executed-models --environment-id 1 --start-date "2024-01-23" --end-date "2024-01-24"
    ```

## mesh_projects

::: dbtc.client.metadata.\_MetadataClient.mesh_projects

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.mesh_projects(1)
    ```

=== "CLI"

    ```bash
    dbtc metadata mesh-projects --account-id 1
    ```

## model_execution_history

::: dbtc.client.metadata.\_MetadataClient.model_execution_history

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.model_execution_history(1, "2024-01-23", "2024-01-24", "model.tpch.dim_customers")
    ```

=== "CLI"

    ```bash
    dbtc metadata model-execution-history --environment-id 1 --start-date "2024-01-23" --end-date "2024-01-24" --unique-id "model.tpch.dim_customers"
    ```

## model_job_information

::: dbtc.client.metadata.\_MetadataClient.model_job_information

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.model_job_information(1, "2024-01-23", "2024-01-24", "model.tpch.dim_customers")
    ```

=== "CLI"

    ```bash
    dbtc metadata model-job-information --environment-id 1 --start-date "2024-01-23" --end-date "2024-01-24" --unique-id "model.tpch.dim_customers"
    ```

## most_executed_models

::: dbtc.client.metadata.\_MetadataClient.most_executed_models

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.most_executed_models(1, "2024-01-23", "2024-01-24")
    ```

=== "CLI"

    ```bash
    dbtc metadata most-executed-models --environment-id 1 --start-date "2024-01-23" --end-date "2024-01-24"
    ```

## most_failed_models

::: dbtc.client.metadata.\_MetadataClient.most_failed_models

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.most_failed_models(1, "2024-01-23", "2024-01-24")
    ```

=== "CLI"

    ```bash
    dbtc metadata most-failed-models --environment-id 1 --start-date "2024-01-23" --end-date "2024-01-24"
    ```

## most_models_test_failures

::: dbtc.client.metadata.\_MetadataClient.most_models_test_failures

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.most_models_test_failures(1, "2024-01-23", "2024-01-24")
    ```

=== "CLI"

    ```bash
    dbtc metadata most-test-failures --environment-id 1 --start-date "2024-01-23" --end-date "2024-01-24"
    ```

## public_models

::: dbtc.client.metadata.\_MetadataClient.public_models

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.public_models(1)
    ```

=== "CLI"

    ```bash
    dbtc metadata public-models --account-id 1
    ```

## search

::: dbtc.client.metadata.\_MetadataClient.search

The `search` method allows you to search across dbt resources in a specific environment.

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.search(
        environment_id=1,
        search_query="customer",
        search_fields=["name", "description"],
        materialization_type="table",
        resource_type="model",
    )
    ```

=== "CLI"

    ```bash
    dbtc metadata search --environment-id 1 --search-query "customer" --materialization-type table --resource-type model
    ```

This method allows for flexible searching across dbt resources with various filtering options. You can specify the number of results, access level, search fields, materialization type, modeling layer, resource type, and tags to refine your search.

## query

::: dbtc.client.metadata.\_MetadataClient.query

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    query = '''
    query ($environmentId: BigInt!, $first: Int!) {
    environment(id: $environmentId) {
        definition {
        metrics(first: $first) {
            edges {
            node {
                name
                description
                type
                formula
                filter
                tags
                parents {
                name
                resourceType
                }
            }
            }
        }
        }
    }
    }
    '''
    variables = {'environmentId': 1, 'first': 500}
    data = client.metadata.query(query, variables)
    client.metadata.query(query, variables)
    ```

## recommendations

::: dbtc.client.metadata.\_MetadataClient.recommendations

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.metadata.recommendations(1)
    ```

=== "CLI"

    ```bash
    dbtc metadata recommendations --environment-id 1
    ```
