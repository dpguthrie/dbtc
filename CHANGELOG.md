# Changelog

## [0.2.0] - 2022-08-30

### Added
- The ability to restart a job from failure.  The `trigger_job` method now accepts an argument `restart_from_failure` (default `False`) that will determine whether or not the last run attempt for a job was unsuccessful - in the event it was, it will parse the steps within that job and find the nodes that it needs to rerun as well as any steps that were skipped entirely.
- Additional commands to the `trigger_job` method:
  - `should_poll` - Indicate whether or not the method should poll for completion (default `True`)
  - `poll_interval` - How long in between polling requests (default 10 seconds)
  - `restart_from_failure` - Described above
  - `trigger_on_failure_only` - Only relevant when setting `restart_from_failure` to `True`.  This has the effect, when set to `True`, of only triggering the job when the prior invocation was not successful.  Otherwise, the function will exit prior to triggering the job (default `False`)
- Logging to stderr when using the `trigger_job` method (internally using the `rich` package that comes when installing `Typer`)
- Multiple tests for the `restart_from_failure` functionality

### Removed
- The `trigger_job_and_poll` method within the `cloud` property of the `dbtCloudClient` class.  The polling functionality is now rolled up into the single `trigger_job` method with the argument `should_poll` (default is `True`)

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
