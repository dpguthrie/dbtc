# Changelog

## [0.11.6]

### Added

-   `include_related` query parameter to the `get_job` method

## [0.11.5]

### Added

-   New `search` method in the metadata client for searching across dbt resources
-   Retry logic to the common session object for the following status codes: 429, 500, 502, 503, 504

### Updated

-   `public_models` method on the `metadata` property - now allows for argument-based filtering.

### Removed

- Rudderstack tracking code

## [0.11.4]

### Fixed

-   Add payload parameter to create_managed_repository

## [0.11.3]

### Added

-   `requiresMetricTime` field to GetMetrics semantic layer query

## [0.11.2]

### Fixed

-   The list_environments method and CLI invocations

## [0.11.1]

### Fixed

-   Versioning issue

## [0.11.0]

### Added

-   New command line groups (e.g. instead of `dbtc list-accounts`, you would use `dbtc accounts list`). Older methods are still around but will be deprecated in future versions.
-   New discovery API convenience methods to retrieve performance, recommendations, and other information

## [0.10.0] - 2024-02-08

### Added

-   Semantic layer client. This can be accessed with the `sl` property on the `dbtCloudClient` class (e.g. `client.sl.query`)

## [0.9.0] - 2024-01-11

### Removed

-   All of the methods in the `_MetadataClient` except for `query`. The Discovery API no longer allows a user to specify every single field recursively, which is what the `sgqlc` package would do.

### Added

-   An optional keyword argument `use_beta_endpoint` to the `dbtCloudClient` class. This will default to `True`, which means that the Discovery API will use the beta endpoint at https://metadata.<host>/beta/graphql instead of https://metadata.<host>/graphql. This contains both the stable API resources (environment, models, tests, etc.) but also contains things for performance, recommendations, and lineage.
-   Ability to automatically paginate requests for the Discovery API. If pagination is required/desired, ensure that your query is properly created with an `$after` variable and all of the fields within the `pageInfo` field.

### Updated

-   Loosen restrictions on Pydantic - ">=2.0,<3.0"

## [0.8.0] - 2023-12-04

### Added

-   `retries` argument to the `trigger_job` method. This will allow you to retry a job `retries` amount of times until completion, which is defined as `success` or `cancelled`.

### Updated

-   `trigger_job_from_failure` method to point at the new `rerun` endpoint. Logic is no longer necessary internally.

## [0.7.0] - 2023-12-04

### Added

-   `output` flag can now be used to pipe output into files instead of stdout

### Removed

-   The `-o` flag is no longer used for order-by when using that argument via the CLI; it is now used as an alternative for output (`--output` or `-o`)

## [0.6.0] - 2023-09-02

### Updated

-   Typer version to `0.9.0`

## [0.5.3] - 2023-08-09

-   Remove read-only field `job_type` from job payload before cloning job

## [0.5.2] - 2023-07-30

### Fixed

-   Method used in the `update_environment_variables` method call from `POST` to `PUT`

## [0.5.1] - 2023-07-30

### Added

-   Methods to update and list environment variables

## [0.5.0] - 2023-07-28

### Fixed

-   `trigger_job_from_failure` method encountering an `IndexError` when called for the first run of the job
-   `assign_user_to_group` method now accepts a `project_id` argument
-   `delete_user_group` method now accepts a `payload` argument

## [0.4.2] - 2023-04-03

### Fixed

-   How the base URL was constructed as it was not properly accounting for other regions, single tenant instances properly

## [0.4.1] - 2023-04-02

### Added

-   Most recent updates for the Metadata API schema

## [0.4.0] - 2023-03-18

### Added

-   List, test, create, get, update, and delete methods for webhooks
-   Support for pydantic models used for validation logic when creating Webhooks - eventually will add support for other create methods
-   Decorator that sets a private property on the `_Client` class, `_called_from`, that helps understand when methods are called from another method.

### Updated

-   `list_users` is now using a v3 endpoint

### Removed

-   All v4 methods were removed as dbt Cloud will begin to deprecate their use soon

## [0.3.7] - 2023-03-04

### Added

-   A `max_run_slots` keyword argument to the `trigger_autoscaling_ci_job` method. This will allow a user to limit the amount of run slots that can be occupied by CI jobs. The default value will be None, which will ensure that the normal behavior of this method remains intact (e.g. it will clone the CI job until the number of run slots configured for the account is reached).

## [0.3.6] - 2023-02-28

### Fixed

-   An additional read-only field from a job definition needed to be removed prior to creating the cloned job. 500 errors were occuring because of this.

## [0.3.5] - 2023-02-22

### Added

-   `version` argument to the CLI. Invoke with `dbtc --version`.
-   Ability to track what methods are being used. Important to note that you can opt out of this by passing `do_not_track=True` to the `dbtCloudClient` class. Additionally, nothing identifiable, like IDs, will be tracked - simply a way to understand what methods of the package are being used.

### Fixed

-   Bad type argument for `poll_interval` in the CLI method for `trigger-job-from-failure`

## [0.3.4] - 2023-01-27

### Added

-   Additional keyword arguments to filter the `list_projects` endpoint by - `project_id`, `state`, `offset`, and `limit`. The `offset` will be useful if an account has greater than 100 (the max projects that can be returned) projects.
-   Additional keyword arguments to filter the `list_jobs` endpoint by - `environment_id`, `state`, `offset`, and `limit`. Important to note that the `project_id` can either be a single project_id integer or a list of project_ids
-   Convenience methods to return the most recent run, `get_most_recent_run`, and the recent run artifact, `get_most_recent_run_artifact`.
-   Additional keyword arguments to filter the `list_environments` endpoint by - `dbt_version`, `name`, `type`, `state`, `offset`, and `limit`. Important to note that the `project_id` can either be a single project_id integer or a list of project_ids.
-   `fields` argument to the methods on the `metadata` property. This allows you to limit the data returned from the Metadata API while still not having to write any GraphQL!
-   `query` method on the `metadata` property. This allows you to write a GraphQL query and supply variables

### Fixed

-   A bug in `get_project_by_name`
-   A bug in the CLI related to any methods that accept the `include_related` argument. This is now valid syntax `'["debug_logs", "run_steps"]'`.

## [0.3.3] - 2022-11-14

### Fixed

-   Autoscaling CI jobs were being improperly cloned when adding a commit to the same PR.

## [0.3.2] - 2022-11-08

### Fixed

-   Finding in progress PR runs using the PR ID within the payload

## [0.3.1] - 2022-11-07

### Fixed

-   In progress runs weren't properly being cancelled within the `trigger_autoscaling_ci_job` method. In addiiton to checking if the job has an in progress run, this method will now also check if there is a run in a "running" state for the PR ID given in the payload. This will ensure that a single PR can only have one run occuring at a given time (this wasn't the case in 0.3.0).

## [0.3.0] - 2022-11-05

### Added

-   `trigger_autoscaling_ci_job` method to the `cloud` property of the `dbtCloudClient` class.

### Changed

-   The restart from failure functionality has now been moved to it's own separate method, `trigger_job_from_failure`. You'll still be able to trigger a job using the `trigger_job` method.

## [0.2.4] - 2022-10-17

### Fixed

-   Non json artifacts are now able to be retrieved from `get_run_artifact`

## [0.2.3] - 2022-09-16

### Fixed

-   Bad url configuration for `create_job` method

## [0.2.2] - 2022-09-15

### Fixed

-   Global CLI args `--warn-error` and `--use-experimental-parser` were not being considered. If they were present in the command, the modified command would have been invalid. These are now included within the `modified_command` if present in the initial step's command.

### Added

-   `--full-refresh` flag is now being pulled in the `modified_command` if present in the initial step's command.

## [0.2.1] - 2022-08-31

### Fixed

-   Checking for an invalid result "skip" instead of "skipped" when identifying nodes that need to be reran.

## [0.2.0] - 2022-08-30

### Added

-   The ability to restart a job from failure. The `trigger_job` method now accepts an argument `restart_from_failure` (default `False`) that will determine whether or not the last run attempt for a job was unsuccessful - in the event it was, it will parse the steps within that job and find the nodes that it needs to rerun as well as any steps that were skipped entirely.
-   Additional commands to the `trigger_job` method:
    -   `should_poll` - Indicate whether or not the method should poll for completion (default `True`)
    -   `poll_interval` - How long in between polling requests (default 10 seconds)
    -   `restart_from_failure` - Described above
    -   `trigger_on_failure_only` - Only relevant when setting `restart_from_failure` to `True`. This has the effect, when set to `True`, of only triggering the job when the prior invocation was not successful. Otherwise, the function will exit prior to triggering the job (default `False`)
-   Logging to stderr when using the `trigger_job` method (internally using the `rich` package that comes when installing `Typer`)
-   Multiple tests for the `restart_from_failure` functionality

### Removed

-   The `trigger_job_and_poll` method within the `cloud` property of the `dbtCloudClient` class. The polling functionality is now rolled up into the single `trigger_job` method with the argument `should_poll` (default is `True`)

## [0.1.4] - 2022-07-11

### Added

-   `get_model_by_environment` to the `metadata` property
-   `meta` field is now available when you query columns

## [0.1.3] - 2022-07-08

### Added

-   The metadata methods are now available via the CLI
-   A `status` arg can now be used in the `list_runs` method on the `cloud` property

## [0.1.2] - 2022-06-30

### Fixed

-   The `_dbt_cloud_request` private method, which is used in the CLI, now only uses `typer.echo` to return data from a request.

### Changed

-   The `trigger_job_and_poll` method now returns the `Run`, represented as a `dict`. It will no longer raise an exception if the result of the run is cancelled or error.

## [0.1.1] - 2022-05-16

### Added

-   The `cloud` property on the `dbtCloudClient` class now contains v3 endpoints

## [0.1.0] - 2022-05-13

### Added

-   `dbtCloudClient` class is the main interface to the dbt Cloud APIs. The `cloud` property contains methods that allow for programmatic access to different resources within dbt Cloud (e.g. `dbtCloudClient().cloud.list_accounts()`). The `metadata` property contains methods that allow for retrieval of metadata related to a dbt Cloud job run (e.g. `dbtCloudClient().metadata.get_models(job_id, run_id)`).
-   `dbtc` is a command line interface to the methods on the `dbtCloudClient` class (e.g. `dbtc list-accounts`)
