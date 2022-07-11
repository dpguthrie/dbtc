# Changelog

## [0.1.4] - 2022-07-11

### Added
- `get_model_by_environment` to the `metadata` property
- `meta` field is now available when you query columns

## [0.1.3] - 2022-07-08

### Added
- The metadata methods are now available via the CLI
- A `status` arg can now be used in the `list_runs` method on the `cloud` property

## [0.1.2] - 2022-06-30

### Fixed
- The `_dbt_cloud_request` private method, which is used in the CLI, now only uses `typer.echo` to return data from a request.

### Changed
- The `trigger_job_and_poll` method now returns the `Run`, represented as a `dict`.  It will no longer raise an exception if the result of the run is cancelled or error.

## [0.1.1] - 2022-05-16

### Added
- The `cloud` property on the `dbtCloudClient` class now contains v3 endpoints

## [0.1.0] - 2022-05-13

### Added
- `dbtCloudClient` class is the main interface to the dbt Cloud APIs.  The `cloud` property contains methods that allow for programmatic access to different resources within dbt Cloud (e.g. `dbtCloudClient().cloud.list_accounts()`).  The `metadata` property contains methods that allow for retrieval of metadata related to a dbt Cloud job run (e.g. `dbtCloudClient().metadata.get_models(job_id, run_id)`).
- `dbtc` is a command line interface to the methods on the `dbtCloudClient` class (e.g. `dbtc list-accounts`)
