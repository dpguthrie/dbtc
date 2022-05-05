# stdlib
import enum
import time
from functools import partial, wraps
from typing import Dict, List

# third party
import requests

# first party
from dbtc_api.client.base import _Client


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


class JobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30


class _CloudClient(_Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.session.headers = self.headers

    _default_domain = 'cloud.getdbt.com'
    _header_property = 'api_key'
    _path = None

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

        Note:  Only available in V4.
        """
        response = self._make_request(path, method=method, **kwargs)
        data = []
        while True:
            response_data = response.json()['data']
            data.extend(response_data) if isinstance(
                response_data, list
            ) else data.extend([response_data])
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

        Note:  Only available in V4.
        """
        return response.headers.get('x-dbt-continuation-token', None)

    @v2
    def list_accounts(self):
        """List of accounts that your API Token is authorized to access."""
        return self._simple_request('accounts/')

    @v2
    def get_account(self, account_id: int):
        """Get an account by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}')

    @v2
    def get_account_licenses(self, account_id: int):
        """List account licenses for a specified account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/licenses')

    @v2
    def list_projects(self, account_id: int):
        """List projects for a specified account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/projects')

    @v2
    def get_project(self, account_id: int, project_id: int):
        """Get a project by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/projects/{project_id}')

    @v2
    def list_jobs(
        self, account_id: int, *, order_by: str = None, project_id: int = None
    ):
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

    @v2
    def create_job(self, account_id: int, payload: Dict):
        """Create job in a given account.

        Args:
            account_id (int): Numeric ID of the account containing the job
            job_id (int): Numeric ID of the job to retrieve
            payload (dict): Payload required for post request
        """
        return self._simple_request(
            f'accounts/{account_id}/jobs/',
            method='post',
            json=payload,
        )

    @v2
    def get_job(self, account_id: int, job_id: int, *, order_by: str = None):
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
    def update_job(self, account_id: int, job_id: int, payload: Dict):
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

    @v2
    def trigger_job(self, account_id: int, job_id: int, payload: Dict):
        """Trigger a job by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to trigger
            payload (dict): Payload required for post request
        """
        return self._simple_request(
            f'accounts/{account_id}/jobs/{job_id}/run/',
            method='post',
            json=payload,
        )

    @staticmethod
    def _run_status_formatted(run_id: int, status: str, time: float) -> str:
        """Format a string indicating status of job.

        Args:
            run_id (int): Numeric ID of the run to retrieve
            status (str): Status of job
            time (float): Elapsed time since job triggered
        """
        return f'Run {run_id} - {status.capitalize()}, Elapsed time: {round(time, 0)}s'

    @v2
    def trigger_job_and_poll(
        self, account_id: int, job_id: int, payload: Dict, poll_interval: int = 10
    ) -> int:
        """Trigger a job by its ID and poll until completion:  one of
          SUCCESS, ERROR, or CANCELLED.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to trigger
            payload (dict): Payload required for post request
            poll_interval (int, optional): Number of seconds to wait in between polling
        """
        run_id = self.trigger_job(account_id, job_id, payload)['data']['id']
        print('Job Triggered!')
        start = time.time()

        while True:
            time.sleep(poll_interval)
            run = self.get_run(account_id, run_id)
            status = run['data']['status']
            status_name = JobRunStatus(status).name
            if status == JobRunStatus.SUCCESS:
                print(
                    self._run_status_formatted(run_id, status_name, time.time() - start)
                )
                return run_id
            if status in [JobRunStatus.CANCELLED, JobRunStatus.ERROR]:
                raise Exception(run['data']['status_message'])
            print(self._run_status_formatted(run_id, status_name, time.time() - start))

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
    ):
        """List runs in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            include_related (List[str], optional): List of related fields to pull with
                the run. Valid values are "trigger", "job", "repository", "debug_logs",
                "run_steps", and "environment".
            job_definition_id (int, optional): Applies a filter to only return runs
                from the specified Job.
            order_by (str, optional): Field to order the result by.
                Use - to indicate reverse order.
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
        """
        return self._simple_request(
            f'accounts/{account_id}/runs',
            params={
                'include_related': ','.join(include_related or []),
                'job_definition_id': job_definition_id,
                'order_by': order_by,
                'offset': offset,
                'limit': limit,
            },
        )

    @v2
    def get_run(
        self, account_id: int, run_id: int, *, include_related: List[str] = None
    ):
        """Get a run by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
            include_related (List[str], optional): List of related fields to pull with
                the run. Valid values are "trigger", "job", "repository", "debug_logs",
                "run_steps", and "environment".
        """
        return self._simple_request(
            f'accounts/{account_id}/runs/{run_id}',
            params={'include_related': ','.join(include_related or [])},
        )

    @v2
    def list_run_artifacts(
        self,
        account_id: int,
        run_id: int,
        *,
        step: int = None,
    ):
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
    def get_run_artifact(
        self,
        account_id: int,
        run_id: int,
        path: str,
        *,
        step: int = None,
    ):
        """Fetch artifacts from a completed run.

        Once a run has completed, you can use this endpoint to download the
        manifest.json, run_results.json or catalog.json files from dbt Cloud. These
        artifacts contain information about the models in your dbt project, timing
        information around their execution, and a status message indicating the result
        of the model build.

        Note: By default, this endpoint returns artifacts from the last step in the
        run. To list artifacts from other steps in the run, use the step query
        parameter described below.

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
        return self._simple_request(
            f'accounts/{account_id}/runs/{run_id}/artifacts/{path}',
            params={'step': step},
        )

    @v2
    def cancel_run(self, account_id: int, run_id: int):
        """Cancel a run.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
        """
        return self._simple_request(
            f'accounts/{account_id}/runs/{run_id}/cancel',
            method='post',
        )

    @v2
    def list_users(
        self,
        account_id: int,
        *,
        limit: int = None,
        offset: int = None,
        order_by: str = 'email',
    ):
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

    @v2
    def list_invited_users(self, account_id: int):
        """List invited users in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/invites/')

    @v2
    def get_user(self, account_id: int, user_id: int):
        """List invited users in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            user_id (int): Numeric ID of the user to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/users/{user_id}/')

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
            limit (int, optional): A limit on the number of objects to be returned,
                between 1 and 100.
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
                'limit': limit or self.limit,
                'environment': environment,
                'project': project,
                'job': job,
                'status': status,
            },
        )

    @v4
    def get_run_v4(self, account_id: int, run_id: int) -> Dict:
        """Retrieves the details of an existing run with the given run_id.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
        """
        return self._simple_request(f'accounts/{account_id}/runs/{run_id}')
