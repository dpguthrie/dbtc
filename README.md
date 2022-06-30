<p align="center">
    <a href="#"><img src="img/dbt.png"></a>
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

**Source Code**: <a target="_blank" href="https://github.com/dpguthrie/dbtc">https://github.com/dpguthrie/dbtc</a>

**V2 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v2">https://docs.getdbt.com/dbt-cloud/api-v2</a>

**V3 Docs (Unofficial)**: <a target="_blank" href="https://documenter.getpostman.com/view/14183654/UVsSNiXC">https://documenter.getpostman.com/view/14183654/UVsSNiXC</a>

**V4 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v4">https://docs.getdbt.com/dbt-cloud/api-v4</a>

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
- [sgqlc]() - Simple GraphQL Client
- [Typer](https://github.com/ross/requests-futures) - Library for building CLI applications

## Installation

```bash
pip install dbtc
```
## Basic Usage

### Python

The interface to both APIs are located in the `dbtCloudClient` class.

The example below shows how you use the `cloud` property on an instance of the `dbtCloudClient` class to access methods that allow for programmatic control over dbt Cloud resources.

```python
from dbtc import dbtCloudClient

client = dbtCloudClient()

account = client.cloud.get_account_by_name('My Account')
project = client.cloud.get_project_by_name(account['id'], 'My Project')

run_id = client.cloud.trigger_job_and_poll()
```

## License

This project is licensed under the terms of the MIT license.
