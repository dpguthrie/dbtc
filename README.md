<p align="center">
    <a href="#"><img src="docs/img/dbt-standalone.png"></a>
</p>
<p align="center">
    <em>An unaffiliated python interface for dbt Cloud APIs</em>
</p>
<p align="center">
    <a href="https://codecov.io/gh/dpguthrie/dbtc" target="_blank">
        <img src="https://img.shields.io/codecov/c/github/dpguthrie/dbtc" alt="Coverage">
    </a>
    <a href="https://pypi.org/project/dbtc" target="_blank">
        <img src="https://badge.fury.io/py/dbtc.svg" alt="Package version">
    </a>
    <a href="https://pepy.tech/project/dbtc" target="_blank">
        <img src="https://pepy.tech/badge/dbtc" alt="Downloads">
    </a>
</p>

---

**Documentation**: <a target="_blank" href="https://dbtc.dpguthrie.com">https://dbtc.dpguthrie.com</a>

**Interactive Demo**: <a target="_blank" href="https://dbtc-python.streamlit.app/">https://dbtc-python.streamlit.app/</a>

**Source Code**: <a target="_blank" href="https://github.com/dpguthrie/dbtc">https://github.com/dpguthrie/dbtc</a>

**V2 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v2">https://docs.getdbt.com/dbt-cloud/api-v2</a>

**V3 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v3">https://docs.getdbt.com/dbt-cloud/api-v3</a>

---

## Overview

dbtc is an unaffiliated python interface to various dbt Cloud API endpoints.

This library acts as a convenient interface to two different APIs that dbt Cloud offers:

-   Cloud API: This is a REST API that exposes endpoints that allow users to programatically create, read, update, and delete
    resources within their dbt Cloud Account.
-   Metadata API: This is a GraphQL API that exposes metadata generated from a job run within dbt Cloud.

## Requirements

Python 3.8+

-   [Requests](https://requests.readthedocs.io/en/master/) - The elegant and simple HTTP library for Python, built for human beings.
-   [sgqlc](https://github.com/profusion/sgqlc) - Simple GraphQL Client
-   [Typer](https://github.com/tiangolo/typer) - Library for building CLI applications

## Installation

```bash
pip install dbtc
```

Or better yet, use [uv](https://docs.astral.sh/uv/)

```bash
uv pip install dbtc
```

## Basic Usage

### Python

The interface to both APIs are located in the `dbtCloudClient` class.

The example below shows how you use the `cloud` property on an instance of the `dbtCloudClient` class to to access a method, `trigger_job_from_failure`, that allows you to restart a job from its last point of failure.

```python
from dbtc import dbtCloudClient

# Assumes that DBT_CLOUD_SERVICE_TOKEN env var is set
client = dbtCloudClient()

account_id = 1
job_id = 1
payload = {'cause': 'Restarting from failure'}

run = client.cloud.trigger_job_from_failure(
    account_id,
    job_id,
    payload,
    should_poll=False,
)

# This returns a dictionary containing two keys
run['data']
run['status']
```

Similarly, use the `metadata` property to retrieve information from the [Discovery API](https://docs.getdbt.com/docs/dbt-cloud-apis/discovery-api).
Here's how you could retrieve all of the metrics for your project.

```python
from dbtc import dbtCloudClient

client = dbtCloudClient()
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

# Data will be in the edges key, which will be a list of nodes
nodes = data['data']['definition']['metrics']['edges']
for node in nodes:
    # node is a dictionary
    node_name = node['name']
    ...
```

If you're unfamiliar either with the Schema to query or even how to write a GraphQL query, I highly recommend going to the [dbt Cloud Discovery API playground](https://metadata.cloud.getdbt.com/beta/graphql). You'll be able to interactively explore the Schema while watching it write a GraphQL query for you!

### CLI

The CLI example below will map to the python cloud example above:

```bash
dbtc trigger-job-from-failure \
    --account-id 1 \
    --job-id 1 \
    --payload '{"cause": "Restarting from failure"}' \
    --no-should-poll
```

Similarly, for the metadata example above (assuming that you've put both the `query` and `variables` argument into variables):

```bash
dbtc query --query $query --variables $variables
```

If not setting your service token as an environment variable, do the following:

```bash
dbtc --token this_is_my_token query --query $query --variables $variables
```

## License

This project is licensed under the terms of the MIT license.
