# Metadata

Every time dbt Cloud runs a project, it generates and stores information about the project. The metadata includes details about your project’s models, sources, and other nodes along with their execution results. With the dbt Cloud Discovery API, you can query this comprehensive information to gain a better understanding of your DAG and the data it produces.

By leveraging the metadata in dbt Cloud, you can create systems for data monitoring and alerting, lineage exploration, and automated reporting. This can help you improve data discovery, data quality, and pipeline operations within your organization.

The `metadata` property on the `dbtCloudClient` class contains a single method, `query`, that allows a user to interact with the [Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api).

If you're unfamiliar either with the Schema to query or even how to write a GraphQL query, I highly recommend going to the [dbt Cloud Discovery API playground](https://metadata.cloud.getdbt.com/beta/graphql).  You'll be able to interactively explore the Schema while watching it write a GraphQL query for you!

## query
::: dbtc.client.metadata._MetadataClient.query

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
