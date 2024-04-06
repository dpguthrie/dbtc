<p align="center">
    <a href="#"><img src="img/dbt-standalone.png"></a>
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

**V3 Docs**: <a target="_blank" href="https://docs.getdbt.com/dbt-cloud/api-v3#/operations/List%20Accounts">https://docs.getdbt.com/dbt-cloud/api-v3#/operations/List%20Accounts</a>

---

## Quick Intro

<div style="position: relative; padding-bottom: 62.5%; height: 0;"><iframe src="https://www.loom.com/embed/7b1a5bf7c9a7410fa970422e8455e404" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## Overview

dbtc is an unaffiliated python interface to various dbt Cloud API endpoints.

This library acts as a convenient interface to two different APIs that dbt Cloud offers:

- **Cloud API**:  This is a REST API that exposes endpoints that allow users to programatically create, read, update, and delete
resources within their dbt Cloud Account.
- **Metadata API**:  This is a GraphQL API that exposes metadata generated from a job run within dbt Cloud.

## Requirements

Python 3.7+

- [Requests](https://requests.readthedocs.io/en/master/) - The elegant and simple HTTP library for Python, built for human beings.
- [Typer](https://github.com/ross/requests-futures) - Library for building CLI applications

## Installation

<div class="termynal" data-termynal data-ty-typeDelay="40" data-ty-lineDelay="700">
    <span data-ty="input">pip install dbtc</span>
    <span data-ty="progress"></span>
    <span data-ty>Successfully installed dbtc</span>
    <a href="#" data-terminal-control="">restart ↻</a>
</div>

## Basic Usage

### Python

The interface to both APIs are located in the `dbtCloudClient` class.

The example below shows how you use the `cloud` property on an instance of the `dbtCloudClient` class to access methods that allow for programmatic control over dbt Cloud resources.

```python
from dbtc import dbtCloudClient

client = dbtCloudClient()

project = client.cloud.get_project(account_id=1, project_id=1)
```

### CLI

All of the methods available via the `dbtCloudClient` class are also available through the command line via `dbtc`.

The same code above can be written as follows using the CLI:

```bash
dbtc get-project --account-id=1 --project-id=1
```

## License

This project is licensed under the terms of the MIT license.
