# Autoscaling CI

!!! warning
    This feature within this package is no longer required as it's all done in a native way with [dbt Cloud's continuous integration](https://docs.getdbt.com/docs/deploy/continuous-integration) offering.

!!! tip "Thank You!"

    As with the [restart from failure](/latest/guide/restart_from_failure) functionality, a lot of credit goes to [@matt-winkler](https://github.com/matt-winkler) for developing this feature.

## Intro

<div style="position: relative; padding-bottom: 57.78491171749599%; height: 0;"><iframe src="https://www.loom.com/embed/5f63e40c356145489a741dac87b47595" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen style="position: absolute; top: 0; left: 0; width: 100%; height: 100%;"></iframe></div>

## Summary

This library offers a convenient interface to create, what we call, an autoscaling CI job.  As of the time of this writing (11/5/22), dbt Cloud does not allow a job to have concurrent runs.  This largely makes sense in the context of regularly scheduled jobs - you would never want your daily job to be run in a concurrent fashion.  However, this feature starts to become a limitation in the context of continuous integration (CI) jobs.  Take the following scenarios:

- Adding a commit to an existing pull request that already has a job running
- Opening a separate pull request in the same repo that already has a running CI job

In both of these instances, we'll have to wait until the existing job has completed before that same CI job can move from a queued state.

## How it Works

In the event your CI job is already running, this package, through the `trigger_autoscaling_ci_job` method, will do the following:

- If a new commit is created for the pull request linked to the existing run for the referenced job, cancel the run and trigger again.
- If this is an entirely new pull request, clone the job definition and trigger the clone.  It's important to note that the cloned job will be deleted by default after the run (you can change this through an argument to the function).  Deleting the cloned job will also force the execution into a polling state (e.g. the function won't return a `Run` until it has encountered a completed state).
- This will also check to see if your account has met or exceeded the allotted run slots.  In the event you have, a cloned job will not be created and the existing job will be triggered.

## Considerations

### dbt Cloud

Normally, when you configure a [dbt Cloud CI job](https://docs.getdbt.com/docs/deploy/cloud-ci-job#slim-ci), you'll do the following:

- Defer to another job
- Include a command with a `state:modified+` selector
- And, trigger it via pull request

To use this functionality, you want to follow all of the steps above **EXCEPT** the trigger piece.  The action that you setup in your repo will take care of triggering the dbt Cloud job, so if you also check that checkbox, you'll be triggering this job in two different places.

### Payload

In order to mimic the native Slim CI behavior within dbt Cloud, it's important to pass the appropriate payload.  The payload should consist of the following (this is in the context of running against a github repository but it will be very similar across Gitlab and ADO).

- `cause` - Put whatever you want here - this is a required field
- `schema_override` - `"dbt_cloud_pr_"$JOB_ID"_"$PULL_REQUEST_ID`
- `git_sha` - `${{ github.event.pull_request.head.sha }}`
- Depending on your git provider, one of `github_pull_request_id`, `gitlab_merge_request_id`, or `azure_pull_request_id` (in the GH action example, set to `${{ github.event.number }}`)

## Recommended Use

This method is best suited to be used within a Github Action, Gitlab CI Pipeline, or an Azure Pipeline.  The example below shows how you can use it within a Github Action.

## Examples

=== "Python"

    ```python
    from dbtc import dbtCloudClient

    # Assumes I have DBT_CLOUD_SERVICE_TOKEN as an environment variable
    client = dbtCloudClient()

    account_id = 1
    job_id = 1
    payload = {
        'cause': 'Autoscaling CI',
        'schema_override': 'dbt_cloud_pr_1_50',
        'github_pull_request_id': 50,
        'git_sha': 'jkafjdkfjallakjf'
    }

    run = client.cloud.trigger_autoscaling_ci_job(account_id, job_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_SERVICE_TOKEN` and `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc trigger-autoscaling-ci-job \
        --job-id=$JOB_ID \
        --payload='{"cause": "Autoscaling Slim CI!","git_sha":"'"$GIT_SHA"'","schema_override":"'"$SO"'","github_pull_request_id":'"$PULL_REQUEST_ID"'}' \
        --no-should-poll)
    ```

=== "Github Action"

    **Required**:  You'll need to create a [secret](https://docs.github.com/en/actions/security-guides/encrypted-secrets#creating-encrypted-secrets-for-a-repository) in your repo called `DBT_CLOUD_SERVICE_TOKEN`.  The token can be obtained from [dbt Cloud](https://docs.getdbt.com/docs/dbt-cloud/dbt-cloud-api/service-tokens)


    ```yaml
    name: Autoscaling dbt Cloud CI
    on:
      pull_request:
        branches:
          - main
        types:
          - opened
          - reopened
          - synchronize
          - ready_for_review

    jobs:
      autoscaling:
        if: github.event.pull_request.draft == false
        runs-on: ubuntu-latest
        env:
          DBT_CLOUD_SERVICE_TOKEN: ${{ secrets.DBT_CLOUD_SERVICE_TOKEN }}
          DBT_CLOUD_ACCOUNT_ID: 43786
          JOB_ID: 73797
          PULL_REQUEST_ID: ${{ github.event.number }}
          GIT_SHA: ${{ github.event.pull_request.head.sha }}

        steps:
          - uses: actions/checkout@v2
          - uses: actions/setup-python@v2
            with:
              python-version: "3.9.x"

          - name: Trigger Autoscaling CI Job
            run: |
              pip install dbtc==0.3.3
              SO="dbt_cloud_pr_"$JOB_ID"_"$PULL_REQUEST_ID
              run=$(dbtc trigger-autoscaling-ci-job \
                --job-id=$JOB_ID \
                --payload='{"cause": "Autoscaling Slim CI!","git_sha":"'"$GIT_SHA"'","schema_override":"'"$SO"'","github_pull_request_id":'"$PULL_REQUEST_ID"'}' \
                --no-should-poll)
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
