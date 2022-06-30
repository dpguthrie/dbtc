# Changelog

## [0.1.1] - 2022-05-16

### Added
- The `cloud` property on the `dbtCloudClient` class now contains v3 endpoints

## [0.1.0] - 2022-05-13

### Added
- `dbtCloudClient` class is the main interface to the dbt Cloud APIs.  The `cloud` property contains methods that allow for programmatic access to different resources within dbt Cloud (e.g. `dbtCloudClient().cloud.list_accounts()`).  The `metadata` property contains methods that allow for retrieval of metadata related to a dbt Cloud job run (e.g. `dbtCloudClient().metadata.get_models(job_id, run_id)`).
- `dbtc` is a command line interface to the methods on the `dbtCloudClient` class (e.g. `dbtc list-accounts`)