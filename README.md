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

**Interactive Demo**: <a target="_blank" href="https://dpguthrie-dbtc-streamlit-home-yy7c0b.streamlit.app/">https://dpguthrie-dbtc-streamlit-home-yy7c0b.streamlit.app/</a>

**Source Code**: <a target="_blank" href="https://github.com/dpguthrie/dbtc">https://github.com/dpguthrie/dbtc</a>

**V2 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v2">https://docs.getdbt.com/dbt-cloud/api-v2</a>

**V3 Docs (Unofficial)**: <a target="_blank" href="https://documenter.getpostman.com/view/14183654/UVsSNiXC">https://documenter.getpostman.com/view/14183654/UVsSNiXC</a>

---

## Overview

dbtc is an unaffiliated python interface to various dbt Cloud API endpoints.

This library acts as a convenient interface to two different APIs that dbt Cloud offers:

- Cloud API:  This is a REST API that exposes endpoints that allow users to programatically create, read, update, and delete
resources within their dbt Cloud Account.
- Metadata API:  This is a GraphQL API that exposes metadata generated from a job run within dbt Cloud.

## Requirements

Python 3.7+

- [Requests](https://requests.readthedocs.io/en/master/) - The elegant and simple HTTP library for Python, built for human beings.
- [sgqlc](https://github.com/profusion/sgqlc) - Simple GraphQL Client
- [Typer](https://github.com/tiangolo/typer) - Library for building CLI applications

## Installation

```bash
pip install dbtc
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

Similarly, use the `metadata` property to retrieve information about certain resources within your project - the example below shows how to retrieve metadata from models related to the most recent run for a given `job_id`.

```python
from dbtc import dbtCloudClient

client = dbtCloudClient()

job_id = 1

models = client.metadata.get_models(job_id)

# Models nested inside a couple keys
models['data']['models']

# This is a list
models['data']['models'][0]
```

### CLI

The CLI example below will map to the python cloud example above:

```bash
dbtc trigger-job-from-failure \
    --account-id 1 \
    --job-id 1 \
    --payload '{"cause": "Restarting from failure"}' \
    --no-should-poll
```

Similarly, for the metadata example above:

```bash
dbtc get-models --job-id 1
```

If not setting your service token as an environment variable, do the following:

```bash
dbtc --token this_is_my_token get_models --job-id 1
```

## License

This project is licensed under the terms of the MIT license.
