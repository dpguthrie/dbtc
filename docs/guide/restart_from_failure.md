# Restart From Failure

!!! warning
    This feature within this package is no longer required as it's all done in a native way through dbt Cloud's [user interface](https://docs.getdbt.com/docs/deploy/retry-jobs) or through the [administrative API](https://docs.getdbt.com/dbt-cloud/api-v2#/operations/Retry%20Failed%20Job)

!!! tip "Thank You!"

    All credit, for both the words below as well as the code that enables this functionality, should be directed to [@matt-winkler](https://github.com/matt-winkler).  The initial work for this started with his incredible [gist](https://gist.github.com/matt-winkler/dcd3004e714648420e0e3bd550222a9d).

## Intro

<div style="position: relative; padding-bottom: 77.41935483870968%; height: 0;"><iframe src="https://www.loom.com/embed/1c1dcf65ba684c5d8ed4607e954c0f4c" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## Summary

This library offers a convenient interface to restart your jobs from the point of failure.  At a high level, it will do the following:

- Inspect the `run_results.json` artifacts from the previous run to understand which nodes succeeded / failed
- Any steps that succeeded on the previous run are skipped
- Any steps that were skipped on the previous run (e.g. because they followed a failed / errored step) are repeated as-is

## Background

dbt Cloud offers users the ability to run and monitor their data pipelines remotely via API endpoints. Each pipeline run produces metadata artifacts that provide rich information on the models run, success/failure status for each, timing, and more.

## Why Pipelines Might Fail

There are a few scenarios in which the need to restart a job from failure occurs in practice:

- Database permission errors
- Code merged to production isn't properly tested (a related-but-separate problem with a distinct set of solutions)
- Data content changes (e.g. due to a problem in a raw data feed that wasn't historically present)
- Timeouts

Despite our best intentions, the above can and will happen.

## How can we Respond to Failures

When responding to failures in a particular area of the DAG, it's often expedient to avoid reprocessing data that's already been run, in particular for maintaining trust with stakeholders when pipelines are "behind." In order to achieve this most efficiently and reliably, the solution should be programmatic, and contained with dbt's capabilities, versus expecting users to:

- Inspect the results of a run to identify the (potentially multiple) roots of failure points (e.g. the earliest failed dbt models or sources for a given run).
- Modify a job command (or create a new job) with the failure points from 1 and including the + syntax to run it's children.
- Ensure the job isn't triggered on an ongoing basis or otherwise put into the orchestration flow unintentionally.

## Examples

=== "Python"

    ```python
    from dbtc import dbtCloudClient

    # Assumes I have DBT_CLOUD_SERVICE_TOKEN as an environment variable
    client = dbtCloudClient()

    account_id = 1
    job_id = 1
    payload = {'cause': 'Restarting from failure'}

    run = client.cloud.trigger_job_from_failure(account_id, job_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_SERVICE_TOKEN` environment variable has been set.
    ```bash
    dbtc trigger-job-from-failure \
        --account-id 1 \
        --job-id 1 \
        --payload '{"cause": "Restarting from failure"}'
    ```

=== "Github Action"

    **Required**:  You'll need to create a [secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) in your repo called `DBT_CLOUD_SERVICE_TOKEN`.  The token can be obtained from [dbt Cloud](https://docs.getdbt.com/docs/dbt-cloud/dbt-cloud-api/service-tokens)


    ```yaml
    name: Restart from Failure
    on:
      workflow_dispatch:

    jobs:
      restart:
        runs-on: ubuntu-latest
        env:
          DBT_CLOUD_SERVICE_TOKEN: ${{ secrets.DBT_CLOUD_SERVICE_TOKEN }}
          DBT_CLOUD_ACCOUNT_ID: 1
          JOB_ID: 1
        # Optional if statement to gate this to a particular user or users
        if: github.actor == 'dpguthrie'
        steps:
          - uses: actions/checkout@v2
          - uses: actions/setup-python@v2
            with:
              python-version: "3.9.x"

          - name: Restart Job from Failure
            run: |
              pip install dbtc==0.3.3
              dbtc trigger-job-from-failure \
                  --job-id=$JOB_ID \
                  --payload='{"cause": "Restarting job from failure"}' \
                  --no-should-poll \
                  --restart-from-failure
    ```

=== "Response"

    ```json
    {
        'status': {
            'code': 200,
            'is_success': True,
            'user_message': 'Success!',
            'developer_message': ''
        },
        'data': {
            'id': 78614274,
            'trigger_id': 79329387,
            'account_id': 1,
            'environment_id': 1,
            'project_id': 1,
            'job_definition_id': 1,
            'status': 1,
            'dbt_version': '1.2.0-latest',
            'git_branch': None,
            'git_sha': None,
            'status_message': None,
            'owner_thread_id': None,
            'executed_by_thread_id': None,
            'deferring_run_id': None,
            'artifacts_saved': False,
            'artifact_s3_path': None,
            'has_docs_generated': False,
            'has_sources_generated': False,
            'notifications_sent': False,
            'blocked_by': [],
            'scribe_enabled': True,
            'created_at': '2022-08-31 02:18:57.855152+00:00',
            'updated_at': '2022-08-31 02:18:57.855169+00:00',
            'dequeued_at': None,
            'started_at': None,
            'finished_at': None,
            'last_checked_at': None,
            'last_heartbeat_at': None,
            'should_start_at': None,
            'trigger': {
                'id': 79329387,
                'cause': 'Just cause',
                'job_definition_id': 1,
                'git_branch': None,
                'git_sha': None,
                'azure_pull_request_id': None,
                'github_pull_request_id': None,
                'gitlab_merge_request_id': None,
                'schema_override': None,
                'dbt_version_override': None,
                'threads_override': None,
                'target_name_override': None,
                'generate_docs_override': None,
                'timeout_seconds_override': None,
                'steps_override': ['dbt run -s bad_model --vars \'{"key": "value"}\''],
                'created_at': '2022-08-31 02:18:57.846515+00:00',
                'cause_humanized': 'Just cause',
                'job': None
            },
            'job': {
                'execution': {
                    'timeout_seconds': 0
                },
                'generate_docs': False,
                'run_generate_sources': False,
                'id': 1,
                'account_id': 1,
                'project_id': 1,
                'environment_id': 1,
                'name': 'Test 10 - Restart with Vars',
                'dbt_version': None,
                'created_at': '2022-08-29T14:02:57.378279Z',
                'updated_at': '2022-08-29T14:06:31.485879Z',
                'execute_steps': ['dbt run -s good_model bad_model --vars \'{"key": "value"}\''],
                'state': 1,
                'deactivated': False,
                'run_failure_count': 0,
                'deferring_job_definition_id': None,
                'lifecycle_webhooks': False,
                'lifecycle_webhooks_url': None,
                'triggers': {
                    'github_webhook': False,
                    'git_provider_webhook': False,
                    'custom_branch_only': False,
                    'schedule': False
                },
                'settings': {
                    'threads': 4,
                    'target_name': 'default'
                },
                'schedule': {
                    'cron': '0 * * * 0,1,2,3,4,5,6',
                    'date': 'days_of_week',
                    'time': 'every_hour'
                },
                'is_deferrable': False
            },
            'environment': None,
            'run_steps': [],
            'status_humanized': 'Queued',
            'in_progress': True,
            'is_complete': False,
            'is_success': False,
            'is_error': False,
            'is_cancelled': False,
            'href': 'https://cloud.getdbt.com/#/accounts/43786/projects/146089/runs/78614274/',
            'duration': '00:00:00',
            'queued_duration': '00:00:00',
            'run_duration': '00:00:00',
            'duration_humanized': '0 minutes',
            'queued_duration_humanized': '0 minutes',
            'run_duration_humanized': '0 minutes',
            'created_at_humanized': '0 minutes ago',
            'finished_at_humanized': '0 minutes from now',
            'job_id': 1,
            'is_running': None
        }
    }
    ```