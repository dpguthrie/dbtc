# Cloud

The `cloud` property on the `dbtCloudClient` class contains methods that allow a user to perform CRUD operations against dbt Cloud resources.

## Accounts

### get_account
::: dbtc.client.admin._AdminClient.get_account

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_account(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc accounts get --account-id 1
    ```

### get_account_by_name
::: dbtc.client.admin._AdminClient.get_account_by_name

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_account_by_name(account_name)
    ```

=== "CLI"

    ```bash
    dbtc accounts get-by-name --account-name "Doug Sandbox"
    ```

### get_account_licenses
::: dbtc.client.admin._AdminClient.get_account_licenses

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_account_licenses(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc accounts get-licenses
    ```

### list_accounts
::: dbtc.client.admin._AdminClient.list_accounts

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_accounts()
    ```

=== "CLI"

    ```bash
    dbtc accounts list
    ```

### list_audit_logs
::: dbtc.client.admin._AdminClient.list_audit_logs

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_audit_logs(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc accounts list-audit-logs
    ```

### list_feature_flags
::: dbtc.client.admin._AdminClient.list_feature_flags

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_feature_flags(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc list-feature-flags
    ```

## Adapters

### create_adapter
::: dbtc.client.admin._AdminClient.create_adapter

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    payload = {
        "id": None,
        "account_id": 1,
        "created_by_id": 1,
        "project_id": 1,
        "state": 1,
        "adapter_version": "databricks_spark_v0"
    }
    client.cloud.create_adapter(1, 1, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc adapters create --payload='{"id": null, "account_id": 1, "created_by_id": 1, "project_id": 1, "state": 1, "adapter_version": "databricks_spark_v0"}'
    ```

### delete_adapter
::: dbtc.client.admin._AdminClient.delete_adapter

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.delete_adapter(1, 1, 1)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc adapters delete --adapter-id 1
    ```

### get_adapter
::: dbtc.client.admin._AdminClient.get_adapter

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_adapter(1, 1, 1)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc adapters get --adapter-id 1
    ```

### update_adapter
::: dbtc.client.admin._AdminClient.update_adapter

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    payload = {
        "id": None,
        "account_id": 1,
        "created_by_id": 1,
        "project_id": 1,
        "state": 1,
        "adapter_version": "databricks_spark_v0"
    }
    client.cloud.update_adapter(1, 1, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc adapters update --payload='{"id": null, "account_id": 1, "created_by_id": 1, "project_id": 1, "state": 1, "adapter_version": "databricks_spark_v0"}'
    ```

## Runs

### get_most_recent_run_artifact
::: dbtc.client.admin._AdminClient.get_most_recent_run_artifact

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_most_recent_run_artifact(account_id, path)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc runs get-most-recent-artifact --path manifest.json
    ```

### get_run_artifact
::: dbtc.client.admin._AdminClient.get_run_artifact

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_run_artifact(account_id, run_id, path)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc runs get-artifact --run-id 1 --path "manifest.json"
    ```

### list_run_artifacts
::: dbtc.client.admin._AdminClient.list_run_artifacts

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_run_artifacts(account_id, run_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc runs list-artifacts --run-id 1
    ```

## Connection

### create_connection
::: dbtc.client.admin._AdminClient.create_connection

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`

    ```py
    client.cloud.create_connection(account_id, project_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.

    ```bash
    dbtc connections create --payload='{"id": null, "name": "<connection-name>", "type": "redshift", "details": {"hostname": "<hostname>", "port": 5439, "dbname": "<your-db-name>", "tunnel_enabled": false}, "state": 1, "account_id": 1, "project_id": 1}'  # noqa: E501
    ```

=== "Snowflake"

    ```py
    payload = {
        'id': None,
        'name': 'Test',
        'type': 'snowflake',
        'details': {
            'account': snowflake_account,
            'role': snowflake_role,
            'database': snowflake_database,
            'warehouse': snowflake_warehouse,
            'oauth_client_id': None,
            'oauth_client_secret': None,
            'client_session_keep_alive': False,
            'allow_sso': False,
        },
        'state': 1,
        'account_id': 1,
        'project_id': 1,
    }
    ```

=== "Bigquery"

    ```py
    payload = {
        'id': None,
        'name': '<test-bigquery-connection>',
        'type': 'bigquery',
        'details': {
            'retries': 1,
            'maximum_bytes_billed': 0,
            'locaiton': None,
            'timeout_seconds': 300,
            'project_id': google_cloud_project_id,
            'private_key_id': service_account_private_key_id,
            'private_key': '-----BEGIN PRIVATE KEY----',
            'client_email': 'service_account_email@gmail.com',
            'client_id': '<service-account-client-id',
            'auth_uri': 'https://accounts.google.com/o/oauth2/auth',
            'token_uri': 'https://oauth2.googleapis.com/token',
            'auth_provider_x509_cert_url': 'https://www.googleapiscom/robot/v1/metadata/x509/<service-account-email>',
            'application_id': None,
            'application_secret': None,
        },
        'state': 1,
        'account_id': 1,
        'project_id': 1,
    }
    ```

=== "Redshift"

    ```py
    payload = {
        'id': None,
        'name': '<connection-name>',
        'type': 'redshift',
        'details': {
            'hostname': '<hostname>',
            'port': 5439,
            'dbname': '<your-db-name>',
            'tunnel_enabled': False,
        },
        'state': 1,
        'account_id': 1,
        'project_id': 1,
    }
    ```

### delete_connection
::: dbtc.client.admin._AdminClient.delete_connection

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.delete_connection(1, 1, 1)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc connections delete --connection-id 1
    ```

### list_connections
::: dbtc.client.admin._AdminClient.list_connections

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`

    ```py
    client.cloud.list_connections(1, 1)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc connections list
    ```

### test_connection
::: dbtc.client.admin._AdminClient.test_connection
### update_connection
::: dbtc.client.admin._AdminClient.update_connection

## Credentials

### create_credentials
::: dbtc.client.admin._AdminClient.create_credentials

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.create_credentials(account_id, project_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc create-credentials --payload='{"id": null, "account_id": 1, "created_by_id": 1, "project_id": 1, "state": 1, "adapter_version": "databricks_spark_v0"}'  # noqa: E501
    ```

=== "Payload"

    ```py
    payload = {
        'id': None,
        'account_id': 1,
        'created_by_id': 1,
        'project_id': 1,
        'state': 1,
        'adapter_version': 'databricks_spark_v0',
    }
    ```

### list_credentials
::: dbtc.client.admin._AdminClient.list_credentials

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_credentials(account_id, project_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc list-credentials
    ```

### update_credentials
::: dbtc.client.admin._AdminClient.update_credentials

## Environment

### create_environment
::: dbtc.client.admin._AdminClient.create_environment
### delete_environment
::: dbtc.client.admin._AdminClient.delete_environment

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.delete_environment(account_id, project_id, environment_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc delete-environment --environment-id=1
    ```

### list_environments
::: dbtc.client.admin._AdminClient.list_environments

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_environments(account_id, project_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc list-environments
    ```

### update_environment
::: dbtc.client.admin._AdminClient.update_environment

## Environment Variables

### create_environment_variables
::: dbtc.client.admin._AdminClient.create_env_vars

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.create_environment_variables(account_id, project_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc create-credentials --payload='{"env_var": {"name": "DBT_ENV_TEST", "ids": [], "new_name": "DBT_ENV_TEST", "project": "foo", "{{development_environment_name}}": "dev_value", "{{deployment_environment_name}}": "deploy_value"}}'
    ```

=== "Payload"

    ```py
    payload = {
        'env_var': {
            'name': 'DBT_ENV_TEST',
            'ids': [],
            'new_name': 'DBT_ENV_TEST',
            'project': 'foo',
            '{{development_environment_name}}': 'dev_value',
            '{{deployment_environment_name}}': 'deploy_value'
        }
    }
    ```

### delete_environment_variables
::: dbtc.client.admin._AdminClient.delete_env_vars

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.delete_environment_variables(account_id, project_id, environment_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc delete-environment --payload='{"name": "DBT_MY_AWESOME_VARIABLE"}'
    ```

=== "Payload"

    ```py
    payload = {
        'name': 'DBT_MY_AWESOME_VARIABLE'
    }
    ```


## Group

### assign_group_permissions
::: dbtc.client.admin._AdminClient.assign_group_permissions

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`

    ```py
    client.cloud.assign_service_token_permissions(account_id, group_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.

    ```bash
    dbtc assign-group-permissions --payload='[{"group_id": 1, "account_id": 1, "permission_set": "analyst", "project_id": 1, "all_projects": false}]'
    ```

=== "Payload"

    ```py
    payload = [
        {
            'group_id': 1,
            'account_id': 1,
            'permission_set': 'analyst',
            'project_id': 1,
            'all_projects': False
        },
    ]
    ```

### assign_user_to_group
::: dbtc.client.admin._AdminClient.assign_user_to_group

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.assign_user_to_group(account_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc assign-user-to-group --payload='{"user_id": 1, "desired_group_ids": [1]}'
    ```

=== "Payload"

    ```py
    payload = {
        'user_id': 1,
        'desired_group_ids': [1],
    }
    ```

### create_user_group
::: dbtc.client.admin._AdminClient.create_user_group

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.create_user_group(account_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc create-user-group --payload='{"account_id": 1, "name": "{{group_name}}", "assign_by_default": false, "sso_mapping_groups": ["mapping_group_1"]}'
    ```

=== "Payload"

    ```py
    payload = {
        'account_id':1,
        'name':'{{group_name}}',
        'assign_by_default':False,
        'sso_mapping_groups':['mapping_group_1']
    }
    ```

### delete_user_group
::: dbtc.client.admin._AdminClient.delete_user_group

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.delete_group(account_id, group_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc delete-environment --group-id=1
    ```

=== "Payload"

    ```py
    payload = {
        'account_id': 1,
        'name': '{{ group_name }}',
        'id': 1,
        'state':2,
        'assign_by_default': False,
        'sso_mapping_groups': []
    }
    ```

### list_groups
::: dbtc.client.admin._AdminClient.list_groups

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_groups(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc list-groups
    ```

## Job

### create_job
::: dbtc.client.admin._AdminClient.create_job

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.create_job(account_id, project_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc create-credentials --payload='{"account_id": 1, "project_id": 1, "id": null, "environment_id": 1, "name": "<your-job-name>", "dbt_version": "1.0.1", "triggers": {"github_webhook": false, "schedule": false, "custom_branch_only": false}, "execute_steps": ["dbt build"], "settings": {"threads": 1, "target_name": "default"}, "state": 1, "generate_docs": false, "schedule": {"date": {"type": "every_day"}, "time": {"type": "every_hour", "interval": 1}}}'
    ```

=== "Payload"

    ```py
    payload = {
        'account_id': 1,
        'project_id': 1,
        'id': None,
        'environment_id': 1,
        'name': '<your-job-name>',
        'dbt_version': '1.0.1',
        'triggers': {
        'github_webhook': False,
        'schedule': False,
        'custom_branch_only': False
        },
        'execute_steps': [
            'dbt build'
        ],
        'settings': {
        'threads': 1,
            'target_name': 'default'
        },
        'state': 1,
        'generate_docs': False,
        'schedule': {
            'date': {
                'type': 'every_day'
            },
            'time': {
                'type': 'every_hour',
                'interval': 1
            }
        }
    }
    ```

### delete_job
::: dbtc.client.admin._AdminClient.delete_job

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.delete_job(account_id, job_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc delete-environment --job-id=1
    ```

### get_job
::: dbtc.client.admin._AdminClient.get_job

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_job(account_id, job_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc get-job --job-id=1
    ```

### list_jobs
::: dbtc.client.admin._AdminClient.list_jobs

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_jobs(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc list-jobs
    ```

### trigger_autoscaling_ci_job
::: dbtc.client.admin._AdminClient.trigger_autoscaling_ci_job

### trigger_job
::: dbtc.client.admin._AdminClient.trigger_job

### trigger_job_from_failure
::: dbtc.client.admin._AdminClient.trigger_job_from_failure

### update_job
::: dbtc.client.admin._AdminClient.update_job

## Repository

### create_repository
::: dbtc.client.admin._AdminClient.create_repository

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.create_repository(account_id, project_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc create-repository --payload='{"account_id": 1, "project_id": 1, "remote_url": "{{git_clone_url}}", "git_clone_strategy": "deploy_key", "github_installation_id": null, "token_str": null}'
    ```

=== "Payload"

    ```py
    payload = {
        'account_id': 1,
        'project_id': 1,
        'remote_url':'{{git_clone_url}}',
        'git_clone_strategy': 'deploy_key',
        'github_installation_id': None,
        'token_str': None
    }
    ```

### delete_repository
::: dbtc.client.admin._AdminClient.delete_repository

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.delete_repository(account_id, project_id, repository_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc delete-repository --repository-id=1
    ```

### list_repositories
::: dbtc.client.admin._AdminClient.list_repositories

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_repositories(account_id, project_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc list-repositories
    ```

### update_repository
::: dbtc.client.admin._AdminClient.update_repository

## Run

### cancel_run
::: dbtc.client.admin._AdminClient.cancel_run

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.cancel_run(account_id, run_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc cancel-run --account-id=1 --run-id=1

### get_most_recent_run
::: dbtc.client.admin._AdminClient.get_most_recent_run

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_most_recent_run(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc get-most-recent-run
    ```

### get_run
::: dbtc.client.admin._AdminClient.get_run

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_run(account_id, run_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc get-run --run-id=1
    ```

### get_run_timing_details
::: dbtc.client.admin._AdminClient.get_run_timing_details

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_run_timing_details(account_id, project_id, run_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc get-run-timing-details --run-id=1
    ```

### list_runs
::: dbtc.client.admin._AdminClient.list_runs

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_runs(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc list-runs
    ```

## Project

### create_project
::: dbtc.client.admin._AdminClient.create_project

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.create_project(account_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc create-project --payload='{"id": null, "name": "{{project_name}}", "dbt_project_subdirectory": null, "account_id": 1, "connection_id": null, "repository_id": null}'
    ```

=== "Payload"

    ```py
    payload = {
        'id': None,
        'name': '{{project_name}}',
        'dbt_project_subdirectory': None,
        'account_id': 1,
        'connection_id': None,
        'repository_id': None
    }
    ```

### delete_project
::: dbtc.client.admin._AdminClient.delete_project

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.delete_project(account_id, project_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc delete-project
    ```

### get_project
::: dbtc.client.admin._AdminClient.get_project

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_project(account_id, project_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc get-project
    ```

### get_project_by_name
::: dbtc.client.admin._AdminClient.get_project_by_name

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_project_by_name(account_id, project_name)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc get-project --project-name=name
    ```

### list_projects
::: dbtc.client.admin._AdminClient.list_projects

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_projects(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc list-projects
    ```

### update_project
::: dbtc.client.admin._AdminClient.update_project

## Service Token

### assign_service_token_permissions
::: dbtc.client.admin._AdminClient.assign_service_token_permissions

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.assign_service_token_permissions(account_id, service_token_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` and `DBT_CLOUD_PROJECT_ID`
    environment variables have been set.
    ```bash
    dbtc assign-service-token-permissions --payload='[{"service_token_id": 1, "account_id": 1, "permission_set": "job_viewer", "project_id": 1, "all_projects": false}]'
    ```

=== "Payload"

    ```py
    payload = [
        {
            'service_token_id': 1,
            'account_id': 1,
            'permission_set': 'job_viewer',
            'project_id': 1,
            'all_projects': False
        },
    ]
    ```

### create_service_token
::: dbtc.client.admin._AdminClient.create_service_token

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.create_service_token(account_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc create-service-token --payload='{"id": null, "name": "api-test", "state": 1, "account_id": 1, "access": {"admin": {"permissionSet": "admin", "projects": [1]}, "job_admin": {"permissionSet": "job_admin", "projects": [1]}}}'
    ```

=== "Payload"

    ```py
    payload = {
        'id': None,
        'name': 'api-test',
        'state': 1,
        'account_id': 1,
        'access': {
            'admin': {
                'permissionSet': 'admin',
                'projects': [
                    1
                ]
            },
            'job_admin': {
                'permissionSet': 'job_admin',
                'projects': [
                    1
                ]
            }
        }
    }
    ```

### get_service_token
::: dbtc.client.admin._AdminClient.get_service_token

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_service_toke (account_id, service_token_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc get-service-token --service-token-id=1
    ```

### list_service_tokens
::: dbtc.client.admin._AdminClient.list_service_tokens

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_service_tokens(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc list-service-tokens
    ```

### list_service_token_permissions
::: dbtc.client.admin._AdminClient.list_service_token_permissions

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_service_token_permissions(account_id, service_token_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc list-service-token-permissions --service-token-id=1
    ```

## User

### deactivate_user_license
::: dbtc.client.admin._AdminClient.deactivate_user_license

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.deactivate_user_license(account_id, permission_id, payload)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc deactivate-user-license --permission_id=1 --payload='{"license_type": "developer", "id": 1, "user_id": 1, "account_id": 1, "state": 2, "groups": [{"account_id": 1, "name": "test-group-with-sso-mappings", "id": 1, "state": 1, "assign_by_default": false, "sso_mapping_groups": ["something"], "group_permissions": [{"account_id": 1, "group_id": 1, "project_id": null, "all_projects": true, "permission_set": "analyst", "permission_level": null, "id": "{{group_permission_id}}", "state": 1}]}], "permission_statements": [{"permission": "invitations_read", "target_resource": null, "all_resources": true}, {"permission": "license_read", "target_resource": null, "all_resources": true}, {"permission": "projects_read", "target_resource": null, "all_resources": true}, {"permission": "environments_read", "target_resource": null, "all_resources": true}, {"permission": "jobs_read", "target_resource": null, "all_resources": true}, {"permission": "runs_read", "target_resource": null, "all_resources": true}, {"permission": "metadata_read", "target_resource": null, "all_resources": true}, {"permission": "custom_environment_variables_read", "target_resource": null, "all_resources": true}, {"permission": "projects_develop", "target_resource": null, "all_resources": true}, {"permission": "credentials_write", "target_resource": null, "all_resources": true}, {"permission": "develop_access", "target_resource": null, "all_resources": true}, {"permission": "custom_environment_variables_write", "target_resource": null, "all_resources": true}]}'
    ```

=== "Payload"

    ```py
    payload = {
        'license_type': 'developer',
        'id': 1,
        'user_id': 1,
        'account_id': 1,
        'state': 2,
        'groups': [
            {
                'account_id': 1,
                'name': 'test-group-with-sso-mappings',
                'id': 1,
                'state': 1,
                'assign_by_default': False,
                'sso_mapping_groups': [
                    'something'
                ],
                'group_permissions': [
                    {
                        'account_id': 1,
                        'group_id': 1,
                        'project_id': None,
                        'all_projects': True,
                        'permission_set': 'analyst',
                        'permission_level': None,
                        'id': '{{group_permission_id}}',
                        'state': 1
                    }
                ]
            }
        ],
        'permission_statements': [
            {
                'permission': 'invitations_read',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'license_read',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'projects_read',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'environments_read',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'jobs_read',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'runs_read',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'metadata_read',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'custom_environment_variables_read',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'projects_develop',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'credentials_write',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'develop_access',
                'target_resource': None,
                'all_resources': True
            },
            {
                'permission': 'custom_environment_variables_write',
                'target_resource': None,
                'all_resources': True
            }
        ]
    }
    ```

### get_user
::: dbtc.client.admin._AdminClient.get_user

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.get_user(account_id, user_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc get_user --user-id=1
    ```

### list_invited_users
::: dbtc.client.admin._AdminClient.list_invited_users

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_invited_users(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc list-invited-users
    ```

### list_users
::: dbtc.client.admin._AdminClient.list_users

**Examples:**
=== "Python"

    Assuming that `client` is an instance of `dbtCloudClient`
    ```py
    client.cloud.list_users(account_id)
    ```

=== "CLI"

    Assuming that `DBT_CLOUD_ACCOUNT_ID` environment variable has been set.
    ```bash
    dbtc list-users
    ```
