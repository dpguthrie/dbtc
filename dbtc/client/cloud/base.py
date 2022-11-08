# stdlib
import argparse
import enum
import json
import shlex
import time
from datetime import datetime
from functools import partial, wraps
from typing import Dict, Iterable, List, Optional, Union

# third party
import requests

# first party
from dbtc.client.base import _Client
from dbtc.utils import listify


class JobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30


PULL_REQUESTS = (
    'github_pull_request_id',
    'gitlab_merge_request_id',
    'azure_pull_request_id',
)


RUN_COMMANDS = ['build', 'run', 'test', 'seed', 'snapshot']
GLOBAL_CLI_ARGS = {
    'warn_error': {'flags': ('--warn-error',), 'action': 'store_true'},
    'use_experimental_parser': {
        'flags': ('--use-experimental-parser',),
        'action': 'store_true',
    },
}
SUB_COMMAND_CLI_ARGS = {
    'vars': {'flags': ('--vars',)},
    'args': {'flags': ('--args',)},
    'fail_fast': {'flags': ('-x', '--fail-fast'), 'action': 'store_true'},
    'full_refresh': {'flags': ('--full-refresh',), 'action': 'store_true'},
    'store_failures': {'flags': ('--store-failures',), 'action': 'store_true'},
}


def _version_decorator(func, version):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._path = f'/api/{version}/'
        result = func(self, *args, **kwargs)
        return result

    return wrapper


v2 = partial(_version_decorator, version='v2')
v3 = partial(_version_decorator, version='v3')
v4 = partial(_version_decorator, version='v4')


class _CloudClient(_Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.session.headers = self.headers
        self.parser = argparse.ArgumentParser()
        all_cli_args = {**GLOBAL_CLI_ARGS, **SUB_COMMAND_CLI_ARGS}
        for arg_specs in all_cli_args.values():
            flags = arg_specs['flags']
            self.parser.add_argument(
                *flags, **{k: v for k, v in arg_specs.items() if k != 'flags'}
            )

    _default_domain = 'cloud.getdbt.com'
    _path = None

    @property
    def _header_property(self):
        if self.api_key is None:
            return 'service_token'

        return 'api_key'

    def _make_request(
        self, path: str, *, method: str = 'get', **kwargs
    ) -> requests.Response:
        """Make request to API."""
        full_url = self.full_url(path)
        response = self.session.request(method=method, url=full_url, **kwargs)
        return response

    def _simple_request(self, path: str, *, method: str = 'get', **kwargs) -> Dict:
        """Return json from response."""
        response = self._make_request(path, method=method, **kwargs)
        return response.json()

    def _paginated_request(
        self, path: str, *, method: str = 'get', **kwargs
    ) -> List[Dict]:
        """Multiple paginated requests given presence of specific header.

        !!! note
            Only available in V4.
        """
        response = self._make_request(path, method=method, **kwargs)
        data = []
        while True:
            response_data = response.json().get('data', [])
            data.extend(response_data)
            next_page_token = self._get_pagination_token(response)
            if next_page_token is not None:
                response = self._make_request(
                    path,
                    method=method,
                    headers={'x-dbt-continuation-token': next_page_token},
                    **kwargs,
                )
            else:
                break
        return data

    def _get_pagination_token(self, response):
        """Retrieve pagination token.

        !!! note
            Only available in V4.
        """
        return response.headers.get('x-dbt-continuation-token', None)

    def _get_by_name(self, items: List, item_name: str, value: str = 'name'):
        try:
            obj = [item for item in items if item[value] == item_name][0]
        except IndexError:
            obj = None
        return obj

    @v3
    def assign_group_permissions(
        self, account_id: int, group_id: int, payload: Dict
    ) -> Dict:
        """Assign group permissions

        Args:
            account_id (int): Numeric ID of the account
            group_id (int): Numeric ID of the group
            payload (dict): Dictionary representing the group to create
        """
        return self._simple_request(
            f'accounts/{account_id}/group-permissions/{group_id}/',
            method='post',
            json=payload,
        )

    @v3
    def assign_service_token_permissions(
        self, account_id: int, service_token_id: int, payload: List[Dict]
    ) -> Dict:
        """Assign permissions to a service token.

        Args:
            account_id (int): Numeric ID of the account
            service_token_id (int): Numeric ID of the service token
            payload (list): List of dictionaries representing the permissions to assign
        """
        return self._simple_request(
            f'accounts/{account_id}/service-tokens/{service_token_id}/permissions/',
            method='post',
            json=payload,
        )

    @v3
    def assign_user_to_group(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Assign a user to a group

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the user to assign
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/assign-groups/',
            method='post',
            json=payload,
        )

    @v2
    def cancel_run(self, account_id: int, run_id: int) -> Dict:
        """Cancel a run.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
        """
        return self._simple_request(
            f'accounts/{account_id}/runs/{run_id}/cancel',
            method='post',
        )

    @v3
    def create_adapter(self, account_id: int, project_id: int, payload: Dict) -> Dict:
        """Create an adapter

        !!! note
            This is a prerequisite for creating a Databricks connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the adapter to create
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/adapters/',
            method='post',
            json=payload,
        )

    @v3
    def create_connection(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the connection to create
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/connections/',
            method='post',
            json=payload,
        )

    @v3
    def create_credentials(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create credentials

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the credentials to create
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/credentials/',
            method='post',
            json=payload,
        )

    @v3
    def create_environment(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create an environment

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the environment to create
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/environments/',
            method='post',
            json=payload,
        )

    @v3
    def create_environment_variables(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create environment variabless

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the environment variables to create
        """
        url = f'accounts/{account_id}/projects/{project_id}/environment-variables/'
        if len(payload.keys()) > 1:
            url += 'bulk/'
        return self._simple_request(url, method='post', json=payload)

    @v2
    def create_job(self, account_id: int, payload: Dict) -> Dict:
        """Create a job

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the job to create
        """
        return self._simple_request(
            f'accounts/{account_id}/jobs/',
            method='post',
            json=payload,
        )

    @v3
    def create_project(self, account_id: int, payload: Dict) -> Dict:
        """Create a project

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the project to create
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/', method='post', json=payload
        )

    @v3
    def create_repository(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create a repository

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the repository to create

        !!! note
            After creating / updating a dbt Cloud repository's SSH key, you will need
            to add the generated key text as a deploy key to the target repository.
            This gives dbt Cloud permissions to read / write in the repository

            You can read more in the [docs](https://docs.getdbt.com/docs/dbt-cloud/cloud-configuring-dbt-cloud/cloud-configuring-repositories)  # noqa: E501
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/repositories/',
            method='post',
            json=payload,
        )

    @v3
    def create_service_token(self, account_id: int, payload: Dict) -> Dict:
        """Create a service token

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the service token to create

        !!! note
            This request creates a service token, but does not assign permissions to
            it.  Permissions are assigned via the
            [assign_service_token_permissions](cloud.md#assign_service_token_permissions)

            See the [user tokens](https://docs.getdbt.com/docs/dbt-cloud/dbt-cloud-api/user-tokens)  # noqa: E501
            and [service tokens](https://docs.getdbt.com/docs/dbt-cloud/dbt-cloud-api/service-tokens)  # noqa: E501
            documentation for more information.
        """
        return self._simple_request(
            f'accounts/{account_id}/service-tokens/', method='post', json=payload
        )

    @v3
    def create_user_group(self, account_id: int, payload: Dict) -> Dict:
        """Create a user group

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the group to create

        !!! note
            The group_name is the name of the dbt Cloud group. The list of
            sso_mapping_groups are string values that dbt Cloud will attempt to match
            with incoming information from your identity provider at login time, in
            order to assign the group with group_name to the user.
        """
        return self._simple_request(
            f'accounts/{account_id}/groups/', method='post', json=payload
        )

    @v2
    def deactivate_user_license(
        self, account_id: int, permission_id: int, payload: Dict
    ) -> Dict:
        """Deactivate user license

        Args:
            account_id (int): Numeric ID of the account
            permission_id (int): Numeric ID of the permission that contains
                user you'd like to deactivate

        !!! note
            Ensure the `groups` object contains all of a user's assigned group
            permissions. This request will fail if a user has already been deactivated.
        """
        return self._simple_request(
            f'accounts/{account_id}/permissions/{permission_id}',
            method='post',
            json=payload,
        )

    @v3
    def delete_connection(
        self, account_id: int, project_id: int, connection_id: int
    ) -> Dict:
        """Delete a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            connection_id (int): Numeric ID of the connection to delete
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/connections/{connection_id}',
            method='delete',
        )

    @v3
    def delete_environment(self, account_id: int, environment_id: int) -> Dict:
        """Delete job for a specified account

        Args:
            account_id (int): Numeric ID of the account
            environment_id (int): Numeric ID of the environment to delete
        """
        return self._simple_request(
            f'accounts/{account_id}/environments/{environment_id}/',
            method='delete',
        )

    @v3
    def delete_environment_variables(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Delete environment variables for a specified account

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (Dict): Dictionary representing environment variables to delete
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/environment-variables/bulk/',
            method='delete',
            json=payload,
        )

    @v2
    def delete_job(self, account_id: int, job_id: int) -> Dict:
        """Delete job for a specified account

        Args:
            account_id (int): Numeric ID of the account
            job_id (int): Numeric ID of the project to delete
        """
        return self._simple_request(
            f'accounts/{account_id}/jobs/{job_id}/',
            method='delete',
        )

    @v3
    def delete_project(self, account_id: int, project_id: int) -> Dict:
        """Delete project for a specified account

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project to delete
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/',
            method='delete',
        )

    @v3
    def delete_repository(
        self, account_id: int, project_id: int, repository_id: int
    ) -> Dict:
        """Delete repository for a specified account

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            repository_id (int): Numeric ID of the repository to delete
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/repositories/{repository_id}',
            method='delete',
        )

    @v3
    def delete_user_group(self, account_id: int, group_id: int) -> Dict:
        """Delete group for a specified account

        Args:
            account_id (int): Numeric ID of the account
            group_id (int): Numeric ID of the group to delete
        """
        return self._simple_request(
            f'accounts/{account_id}/groups/{group_id}/',
            method='post',
        )

    @v2
    def get_account(self, account_id: int) -> Dict:
        """Get an account by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}')

    @v2
    def get_account_by_name(self, account_name: str) -> Dict:
        """Get an account by its name.

        Args:
            account_name (str): Name of an account
        """
        accounts = self.list_accounts()
        account = self._get_by_name(accounts['data'], account_name)
        if account is not None:
            return self.get_account(account['id'])

        raise Exception(f'"{account_name}" was not found')

    @v2
    def get_account_licenses(self, account_id: int) -> Dict:
        """List account licenses for a specified account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/licenses')

    @v2
    def get_job(self, account_id: int, job_id: int, *, order_by: str = None) -> Dict:
        """Get a job by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to retrieve
            order_by (str, optional): Field to order the result by.
                Use - to indicate reverse order.
        """
        return self._simple_request(
            f'accounts/{account_id}/jobs/{job_id}/',
            params={'order_by': order_by},
        )

    @v2
    def get_project(self, account_id: int, project_id: int) -> Dict:
        """Get a project by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/projects/{project_id}')

    @v2
    def get_project_by_name(
        self, project_name: str, account_id: int = None, account_name: str = None
    ) -> Dict:
        """Get a project by its name.

        Args:
            project_name (str): Name of project to retrieve
            account_id (int, optional): Numeric ID of the account to retrieve
            account_name (str, optional): Name of account to retrieve
        """
        if account_id is None and account_name is None:
            accounts = self.list_accounts()
            for account in accounts['data']:
                projects = self.list_projects(account['id'])
                project = self._get_by_name(projects['data'], project_name)
                if project is not None:
                    break

        else:
            if account_id is not None:
                account = self.get_account(account_id)
            else:
                account = self.get_account_by_name(account_name)
            projects = self.list_projects(account['id'])
            project = self._get_by_name(projects['data'], project_name)

        if project is not None:
            return self.get_project(project['account_id'], project['id'])

        raise Exception(f'"{project_name}" was not found.')

    @v2
    def get_run(
        self, account_id: int, run_id: int, *, include_related: List[str] = None
    ) -> Dict:
        """Get a run by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
            include_related (list): List of related
                fields to pull with the run. Valid values are `trigger`, `job`,
                `repository`, `debug_logs`, `run_steps`, and `environment`.
        """
        return self._simple_request(
            f'accounts/{account_id}/runs/{run_id}',
            params={'include_related': ','.join(include_related or [])},
        )

    @v2
    def get_run_artifact(
        self,
        account_id: int,
        run_id: int,
        path: str,
        *,
        step: int = None,
    ) -> Union[str, Dict]:
        """Fetch artifacts from a completed run.

        Once a run has completed, you can use this endpoint to download the
        `manifest.json`, `run_results.json` or `catalog.json` files from dbt Cloud.
        These artifacts contain information about the models in your dbt project,
        timing information around their execution, and a status message indicating the
        result of the model build.

        !!! note
            By default, this endpoint returns artifacts from the last step in the
            run. To list artifacts from other steps in the run, use the step query
            parameter described below.

        !!! warning
            If requesting a non JSON artifact, the result will be a `str`

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
            path (str): Paths are rooted at the target/ directory. Use manifest.json,
                catalog.json, or run_results.json to download dbt-generated artifacts
                for the run.
            step (str, optional): The index of the Step in the Run to query for
                artifacts. The first step in the run has the index 1. If the step
                parameter is omitted, then this endpoint will return the artifacts
                compiled for the last step in the run.
        """
        url_path = f'accounts/{account_id}/runs/{run_id}/artifacts/{path}'
        params = {'step': step}
        if path[-5:] == '.json':
            return self._simple_request(url_path, params=params)

        response = self._make_request(url_path, params=params)
        return response.text

    @v3
    def get_run_timing_details(
        self, account_id: int, project_id: int, run_id: int
    ) -> Dict:
        """Retrieves the timing details related to a run

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/runs/{run_id}/timing/'
        )

    @v4
    def get_run_v4(self, account_id: int, run_id: int) -> Dict:
        """Retrieves the details of an existing run with the given run_id.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/runs/{run_id}')

    @v3
    def get_service_token(self, account_id: int, service_token_id: int) -> Dict:
        """Retrieves a service token.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            service_token_id (int): Numeric ID of the service token to retrieve
        """
        return self._simple_request(
            f'accounts/{account_id}/service-tokens/{service_token_id}'
        )

    @v2
    def get_user(self, account_id: int, user_id: int) -> Dict:
        """List invited users in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            user_id (int): Numeric ID of the user to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/users/{user_id}/')

    @v2
    def list_accounts(self) -> Dict:
        """List of accounts that your API Token is authorized to access."""
        return self._simple_request('accounts/')

    @v3
    def list_audit_logs(
        self,
        account_id: int,
        *,
        logged_at_start: str = None,
        logged_at_end: str = None,
        offset: int = None,
        limit: int = None,
    ) -> Dict:
        """List audit logs for a specific account

        Args:
            account_id (int): Numeric ID of the account to retrieve
            logged_at_start (str, optional):  Date to begin retrieving audit
                logs
                Format is yyyy-mm-dd
            logged_at_end (str, optional): Date to stop retrieving audit logs.
                Format is yyyy-mm-dd
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
        """
        return self._simple_request(
            f'accounts/{account_id}/audit-logs',
            params={
                'logged_at_start': logged_at_start,
                'logged_at_end': logged_at_end,
                'offset': offset,
                'limit': limit,
            },
        )

    @v3
    def list_connections(self, account_id: int, project_id: int) -> Dict:
        """List connections for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/connections'
        )

    @v3
    def list_credentials(self, account_id: int, project_id: int) -> Dict:
        """List credentials for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/credentials'
        )

    @v3
    def list_environments_by_account(self, account_id: int) -> Dict:
        """List environments for a specific account

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/environments/')

    @v3
    def list_environments(self, account_id: int, project_id: int = None) -> Dict:
        """List environments for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int, optional): Numeric ID of the project to retrieve
        """
        uri = f'accounts/{account_id}/'
        if project_id is not None:
            uri += f'projects/{project_id}/'
        uri += 'environments/'
        return self._simple_request(uri)

    @v3
    def list_feature_flags(self, account_id: int) -> Dict:
        """List feature flags for a specific account

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/feature-flag/')

    @v3
    def list_groups(self, account_id: int) -> Dict:
        """List groups for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/groups/')

    @v2
    def list_invited_users(self, account_id: int) -> Dict:
        """List invited users in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/invites/')

    @v2
    def list_jobs(
        self, account_id: int, *, order_by: str = None, project_id: int = None
    ) -> Dict:
        """List jobs in an account or specific project.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            order_by (str, optional): Field to order the result by.
                Use - to indicate reverse order.
            project_id (int, optional): Numeric ID of the project containing jobs
        """
        return self._simple_request(
            f'accounts/{account_id}/jobs/',
            params={'order_by': order_by, 'project_id': project_id},
        )

    @v3
    def list_projects(self, account_id: int) -> Dict:
        """List projects for a specified account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/projects')

    @v3
    def list_repositories(self, account_id: int, project_id: int) -> Dict:
        """List repositories for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/repositories/'
        )

    @v2
    def list_run_artifacts(
        self,
        account_id: int,
        run_id: int,
        *,
        step: int = None,
    ) -> Dict:
        """Fetch a list of artifact files generated for a completed run.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
            step (str, optional): The index of the Step in the Run to query for
                artifacts. The first step in the run has the index 1. If the step
                parameter is omitted, then this endpoint will return the artifacts
                compiled for the last step in the run.
        """
        return self._simple_request(
            f'accounts/{account_id}/runs/{run_id}/artifacts',
            params={'step': step},
        )

    @v2
    def list_runs(
        self,
        account_id: int,
        *,
        include_related: List[str] = None,
        job_definition_id: int = None,
        order_by: str = None,
        offset: int = None,
        limit: int = None,
        status: Union[List[str], str] = None,
    ) -> Dict:
        """List runs in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            include_related (list): List of related
                fields to pull with the run. Valid values are `trigger`, `job`,
                `repository`, `debug_logs`, `run_steps`, and `environment`.
            job_definition_id (int, optional): Applies a filter to only return
                runs
                from the specified Job.
            order_by (str, optional): Field to order the result by.
                Use - to indicate reverse order.
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
            status (str or list, optional): The status to apply when listing runs.
                Options include queued, starting, running, success, error, and
                cancelled
        """
        if status is not None:
            try:
                status = [getattr(JobRunStatus, s.upper()) for s in listify(status)]
            except AttributeError:
                raise
            else:
                status = json.dumps(status)
        return self._simple_request(
            f'accounts/{account_id}/runs',
            params={
                'include_related': ','.join(include_related or []),
                'job_definition_id': job_definition_id,
                'order_by': order_by,
                'offset': offset,
                'limit': limit,
                'status__in': status,
            },
        )

    @v4
    def list_runs_v4(
        self,
        account_id: int,
        *,
        limit: int = None,
        environment: str = None,
        project: str = None,
        job: str = None,
        status: str = None,
    ) -> List[Dict]:
        """Returns a list of runs in the account.

        The runs are returned sorted by creation date, with the most recent run
        appearing first.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            limit (int, optional): A limit on the number of objects to be
                returned, between 1 and 100.
            environment (str): A filter on the list based on the object's
                environment_id field.
            project (str): A filter on the list based on the object's project_id field.
            job (str): A filter on the list based on the object's job_id field.
            status: A filter on the list based on the object's status field.
                Enum: "Queued" "Starting" "Running" "Succeeded" "Failed" "Canceled"
        """
        return self._paginated_request(
            f'accounts/{account_id}/runs',
            params={
                'limit': limit,
                'environment': environment,
                'project': project,
                'job': job,
                'status': status,
            },
        )

    @v3
    def list_service_token_permissions(
        self, account_id: int, service_token_id: int
    ) -> Dict:
        """List service token permissions for a specific account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            service_token_id (int): Numeric ID of the service token to retrieve
        """
        return self._simple_request(
            f'accounts/{account_id}/service-tokens/{service_token_id}/permissions'
        )

    @v3
    def list_service_tokens(self, account_id: int) -> Dict:
        """List service tokens for a specific account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/service-tokens/')

    @v2
    def list_users(
        self,
        account_id: int,
        *,
        limit: int = None,
        offset: int = None,
        order_by: str = 'email',
    ) -> Dict:
        """List users in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            order_by (str, optional): Field to order the result by.
                Use - to indicate reverse order.
        """
        return self._simple_request(
            f'accounts/{account_id}/users/',
            params={'limit': limit, 'offset': offset, 'order_by': order_by},
        )

    @v3
    def test_connection(self, account_id: int, payload: Dict) -> Dict:
        """Test a connection

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the connection to test
        """
        return self._simple_request(
            f'accounts/{account_id}/connections/test/', method='post', json=payload
        )

    @v2
    def trigger_autoscaling_ci_job(
        self,
        account_id: int,
        job_id: int,
        payload: Dict,
        *,
        should_poll: bool = False,
        poll_interval: int = 10,
        delete_cloned_job: bool = True,
    ):
        """Trigger an autoscaling CI job

        !!! info

            In the event your CI job is already running, this will do the following:

            - If a new commit is created for the currently running job, cancel the
              job and then trigger again
            - If this is an entirely new pull request, clone the job and trigger
            - This will also check to see if your account has met or exceeded the
              allotted run slots.  In the event you have, a cloned job will
              not be created and the existing job will be triggered.

        More info [here](/latest/guide/autoscaling_ci)

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to trigger
            payload (dict): Payload required in triggering a job.  It's important that
                the payload consists of the following keys in order to mimic the
                native behavior of dbt Cloud's Slim CI functionality:

                - `git_sha`
                - `cause`
                - `schema_override`
                - Depending on your git provider, one of `github_pull_request_id`,
                  `gitlab_merge_request_id`, or `azure_pull_request_id`
            should_poll (bool, optional): Poll until completion if `True`, completion
                is one of success, failure, or cancelled
            poll_interval (int, optional): Number of seconds to wait in between
                polling
            delete_cloned_job (bool, optional): Indicate if cloned job should be
                deleted after being triggered
        """
        self.console.log('Finding any in progress runs...')
        cloned_job = None
        payload_pr_id = None
        pull_request_key: Optional[str] = None

        # Get all runs in "running" state
        in_progress_runs = self.list_runs(
            account_id,
            status=['queued', 'starting', 'running'],
            include_related=['trigger'],
        ).get('data', [])

        # Find any runs that match the job_id specified in function signature
        in_progress_job_run = [
            r for r in in_progress_runs if r.get('job_definition_id', -1) == job_id
        ]

        # Find the valid pull_request_key to use in pulling out relevant PR IDs
        for pull_request_key in PULL_REQUESTS:
            if pull_request_key in payload:
                payload_pr_id = payload[pull_request_key]
                break
        else:
            pull_request_key = None

        # This will be used to identify if the PR within the payload has a run
        # that's in a running state.
        in_progress_pr_run = [
            r
            for r in in_progress_runs
            if r.get('trigger', {}).get(pull_request_key, -1) == payload_pr_id
        ]

        if in_progress_pr_run:

            # A PR should only have one run in a queued, running, or starting state
            # at any given time
            run = in_progress_pr_run[0]
            self.console.log(
                f'Found an in progress run for PR #{payload_pr_id}.  Run {run["id"]} '
                'will be canceled and a job triggered for the new commit.'
            )
            _ = self.cancel_run(account_id, run['id'])

        if in_progress_job_run:
            self.console.log(f'Found an in progress run for job {job_id}.')

            # Job can only have one run in a queued, running, or starting state
            run = in_progress_job_run[0]

            acct = self.get_account(account_id).get('data', {})
            run_slots = acct.get('run_slots', 0)
            if run_slots > len(in_progress_runs):
                self.console.log(
                    f'Job {job_id} is currently being used in run {run["id"]}. '
                    'This job definition will be cloned and then triggered for '
                    f'pull request #{payload_pr_id}.'
                )
                current_job = self.get_job(account_id, job_id).get('data', {})

                # Alter the current job definition so it can be cloned
                current_job.pop('is_deferrable')
                current_job['id'] = None
                now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                current_job['name'] = current_job['name'] + f' [CLONED {now}]'
                cloned_job = self.create_job(account_id, current_job)['data']

                # Modify the should_poll argument - this needs to be `True`
                # if we're deleting the cloned job.  Otherwise, dbt Cloud
                # will cancel the run because it can't find an associated job
                if delete_cloned_job:
                    should_poll = True
                job_id = cloned_job['id']
            else:
                self.console.log(
                    'Not cloning the job as your account has met or exceeded the '
                    'number of run slots and will not be able to execute even a '
                    'cloned CI job.'
                )
        else:
            self.console.log('No in progress job run found.  Triggering as normal')
        run = self.trigger_job(
            account_id,
            job_id,
            payload,
            should_poll=should_poll,
            poll_interval=poll_interval,
        )
        if cloned_job is not None and delete_cloned_job:
            self.delete_job(account_id, job_id)
        return run

    @v2
    def trigger_job_from_failure(
        self,
        account_id: int,
        job_id: int,
        payload: Dict,
        *,
        should_poll: bool = True,
        poll_interval: bool = False,
        trigger_on_failure_only: bool = True,
    ):
        """Restart a job from the point of failure

        More info [here](/latest/guide/restart_from_failure)

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to trigger
            payload (dict): Payload required for post request
            should_poll (bool, optional): Poll until completion if `True`, completion
                is one of success, failure, or cancelled
            poll_interval (int, optional): Number of seconds to wait in between
                polling
            trigger_on_failure_only (bool, optional): Only relevant when setting
                restart_from_failure to True.  This has the effect of only triggering
                the job when the prior invocation was not successful. Otherwise, the
                function will exit prior to triggering the job.
        """

        def parse_args(cli_args: Iterable[str], namespace: argparse.Namespace):
            string = ''
            for arg in cli_args:
                value = getattr(namespace, arg, None)
                if value:
                    arg = arg.replace('_', '-')
                    if isinstance(value, bool):
                        string += f' --{arg}'
                    else:
                        string += f" --{arg} '{value}'"
            return string

        self.console.log(f'Restarting job {job_id} from last failed state.')
        last_run_data = self.list_runs(
            account_id=account_id,
            include_related=['run_steps'],
            job_definition_id=job_id,
            order_by='-id',
            limit=1,
        )['data'][0]

        last_run_status = last_run_data['status_humanized'].lower()
        last_run_id = last_run_data['id']

        if last_run_status == 'error':
            rerun_steps = []
            job_info = self.get_job(account_id, job_id)['data']
            generate_docs = job_info.get('generate_docs', False)
            generate_sources = job_info.get('generate_sources', False)
            for run_step in last_run_data['run_steps']:

                status = run_step['status_humanized'].lower()
                # Skipping cloning, profile setup, and dbt deps - always
                # the first three steps in any run
                if run_step['index'] <= 3 or status == 'success':
                    self.console.log(
                        f'Skipping rerun for command "{run_step["name"]}" '
                        'as it does not need to be repeated.'
                    )
                    continue

                else:

                    # get the dbt command used within this step
                    # Example:  Get dbt build from "Invoke dbt with `dbt build`"
                    command = run_step['name'].partition('`')[2].partition('`')[0]
                    freshness_in_command = (
                        'dbt source snapshot-freshness' in command
                        or 'dbt source freshness' in command
                    )
                    if 'dbt docs generate' in command and generate_docs:
                        continue
                    elif freshness_in_command and generate_sources:
                        continue

                    namespace, remaining = self.parser.parse_known_args(
                        shlex.split(command)
                    )
                    sub_command = remaining[1]
                    is_run_command = sub_command in RUN_COMMANDS
                    is_not_success = status in ('error', 'skipped', 'cancelled')
                    is_skipped = status == 'skipped'
                    if (not is_run_command and is_not_success) or (
                        is_run_command and is_skipped
                    ):
                        rerun_steps.append(command)

                    # errors and failures are when we need to inspect to figure
                    # out the point of failure
                    else:

                        # get the run results scoped to the step which had an error
                        # an error here indicates that either:
                        # 1) the fail-fast flag was set, in which case
                        #    the run_results.json file was never created; or
                        # 2) there was a problem on dbt Cloud's side saving
                        #    this artifact
                        try:
                            step_results = self.get_run_artifact(
                                account_id=account_id,
                                run_id=last_run_id,
                                path='run_results.json',
                                step=run_step['index'],
                            )['results']

                        # If the artifact isn't found, the API returns a 404 with
                        # no json.  The ValueError will catch the JSONDecodeError
                        except ValueError:
                            rerun_steps.append(command)
                        else:
                            rerun_nodes = ' '.join(
                                record['unique_id'].split('.')[2]
                                for record in step_results
                                if record['status'] in ['error', 'skipped', 'fail']
                            )
                            global_args = parse_args(GLOBAL_CLI_ARGS.keys(), namespace)
                            sub_command_args = parse_args(
                                SUB_COMMAND_CLI_ARGS.keys(), namespace
                            )
                            modified_command = f'dbt{global_args} {sub_command} -s {rerun_nodes}{sub_command_args}'  # noqa: E501
                            rerun_steps.append(modified_command)
                            self.console.log(
                                f'Modifying command "{command}" as an error '
                                'or failure was encountered.'
                            )

            payload.update({"steps_override": rerun_steps})
            self.console.log(
                f'Triggering modified job to re-run failed steps: {rerun_steps}'
            )

        else:
            self.console.log(
                'Process triggered with restart_from_failure set to True but no '
                'failed run steps found.'
            )
            if trigger_on_failure_only:
                self.console.log('Not triggering job because prior run was successful.')
                return
        return self.trigger_job(
            account_id,
            job_id,
            payload,
            should_poll=should_poll,
            poll_interval=poll_interval,
        )

    @v2
    def trigger_job(
        self,
        account_id: int,
        job_id: int,
        payload: Dict,
        *,
        should_poll: bool = True,
        poll_interval: int = 10,
    ):
        """Trigger a job by its ID

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to trigger
            payload (dict): Payload required for post request
            should_poll (bool, optional): Poll until completion if `True`, completion
                is one of success, failure, or cancelled
            poll_interval (int, optional): Number of seconds to wait in between
                polling
        """

        def run_status_formatted(run: Dict, time: float) -> str:
            """Format a string indicating status of job.
            Args:
                run (dict): Dictionary representation of a Run
                time (float): Elapsed time since job triggered
            """
            status = JobRunStatus(run['data']['status']).name
            url = run['data']['href']
            return (
                f'Status: "{status.capitalize()}", Elapsed time: {round(time, 0)}s'
                f', View here: {url}'
            )

        run = self._simple_request(
            f'accounts/{account_id}/jobs/{job_id}/run/',
            method='post',
            json=payload,
        )
        if not run['status']['is_success']:
            self.console.log(f'Run NOT triggered for job {job_id}.  See run response.')
            return run

        self.console.log(run_status_formatted(run, 0))
        if should_poll:
            start = time.time()
            run_id = run['data']['id']
            while True:
                time.sleep(poll_interval)
                run = self.get_run(account_id, run_id)
                status = run['data']['status']
                self.console.log(run_status_formatted(run, time.time() - start))
                if status in [
                    JobRunStatus.SUCCESS,
                    JobRunStatus.CANCELLED,
                    JobRunStatus.ERROR,
                ]:
                    break

        return run

    @v3
    def update_connection(
        self, account_id: int, project_id: int, connection_id: int, payload: Dict
    ) -> Dict:
        """Update a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            connection_id (int): Numeric ID of the connection to update
            payload (dict): Dictionary representing the connection to update
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/connections/{connection_id}/',
            method='post',
            json=payload,
        )

    @v3
    def update_credentials(
        self, account_id: int, project_id: int, credentials_id: int, payload: Dict
    ) -> Dict:
        """Update credentials

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            credentials_id (int): Numeric ID of the credentials to update
            payload (dict): Dictionary representing the credentials to update
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/credentials/{credentials_id}/',  # noqa: E50
            method='post',
            json=payload,
        )

    @v3
    def update_environment(
        self, account_id: int, project_id: int, environment_id: int, payload: Dict
    ) -> Dict:
        """Update a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            environment_id (int): Numeric ID of the environment to update
            payload (dict): Dictionary representing the environment to update
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/environments/{environment_id}/',  # noqa: E501
            method='post',
            json=payload,
        )

    @v2
    def update_job(self, account_id: int, job_id: int, payload: Dict) -> Dict:
        """Update a job by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to retrieve
            payload (dict): Payload required for post request
        """
        return self._simple_request(
            f'accounts/{account_id}/jobs/{job_id}/',
            method='post',
            json=payload,
        )

    @v3
    def update_project(self, account_id: int, project_id: int, payload: Dict) -> Dict:
        """Update project for a specified account

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project to update
            payload (dict): Dictionary representing the project to update
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/', method='POST', json=payload
        )

    @v3
    def update_repository(
        self, account_id: int, project_id: int, repository_id: int, payload: Dict
    ) -> Dict:
        """Update a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            repository_id (int): Numeric ID of the repository to update
            payload (dict): Dictionary representing the repository to update
        """
        return self._simple_request(
            f'accounts/{account_id}/projects/{project_id}/repositories/{repository_id}/',  # noqa: E501
            method='post',
            json=payload,
        )
