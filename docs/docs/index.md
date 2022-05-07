<p align="center">
    <a href="#"><img src="docs/docs/img/full.png"></a>
</p>
<p align="center">
    <em>An unaffiliated python wrapper for dbt Cloud APIs</em>
</p>
<p align="center">
    <a href="https://codecov.io/gh/dpguthrie/dbtc-api" target="_blank">
        <img src="https://img.shields.io/codecov/c/github/dpguthrie/dbtc-api" alt="Coverage">
    </a>
</p>

---

**Documentation**: <a target="_blank" href="https://dbtc.dpguthrie.com">https://dbtc.dpguthrie.com</a>

**Source Code**: <a target="_blank" href="https://github.com/dpguthrie/dbtc-api">https://github.com/dpguthrie/dbtc-api</a>

**V2 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v2">https://docs.getdbt.com/dbt-cloud/api-v2</a>

**V3 Docs (Unofficial)**: <a target="_blank" href="https://documenter.getpostman.com/view/14183654/UVsSNiXC">https://documenter.getpostman.com/view/14183654/UVsSNiXC</a>

**V4 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v4">https://docs.getdbt.com/dbt-cloud/api-v4</a>

---

## Overview

dbtc-api is an unaffiliated python interface to various dbt Cloud API endpoints.

## Requirements

Python 3.7+

- [Requests](https://requests.readthedocs.io/en/master/) - The elegant and simple HTTP library for Python, built for human beings.
- [sgqlc]() - Simple GraphQL Client
- [Typer](https://github.com/ross/requests-futures) - Library for building CLI applications

## Installation

```bash
pip install dbtc
```
## Example

There are two sets of APIs that dbt Cloud offers:

- Cloud -
- Metadata

```python
from dbtc import dbtCloudClient

client = dbtCloudClient()

accounts = client.cloud.list_accounts()
account_id = accounts['data'][0]['id']

projects = client.cloud.list_projects(account_id)

```

## Multiple Symbol Example

The `Ticker` class also makes it easy to retrieve data for a list of symbols with the same API. Simply pass a list of symbols as the argument to the `Ticker` class.

```python
from yahooquery import Ticker

symbols = ['fb', 'aapl', 'amzn', 'nflx', 'goog']

faang = Ticker(symbols)

faang.summary_detail
```

## License

This project is licensed under the terms of the MIT license.