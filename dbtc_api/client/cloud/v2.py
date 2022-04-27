# stdlib
import enum
import time
from typing import Dict, List

# first party
from dbtc_api.client.cloud.base import _CloudClient


class JobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30


class _CloudClientV2(_CloudClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    _default_domain = 'cloud.getdbt.com'
    _path = '/api/v2/'

    def list_accounts(self):
        """List of accounts that your API Token is authorized to access."""
        return self._make_request('accounts')

    def get_account(self, account_id: int):
        """Get an account by its ID

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._make_request(f'accounts/{account_id}')

    def get_account_licenses(self, account_id: int):
        return self._make_request(f'accounts/{account_id}/licenses')

    def list_projects(self, account_id: int):
        """List projects for a specified account

        Args:
            account_id (int): Numerc ID of the account to retrieve
        """
        return self._make_request(f'accounts/{account_id}/projects')

    def get_project(self, account_id: int, project_id: int):
        """Get a project by its ID

        Args:
            account_id (int): Numerc ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
        """
        return self._make_request(f'accounts/{account_id}/projects/{project_id}')

    def list_jobs(
        self, account_id: int, *, order_by: str = None, project_id: int = None
    ):
        """List jobs in an account or specific project

        Args:
            account_id (int): Numerc ID of the account to retrieve
            order_by (:obj:`str`, optional): Field to order the result by.
                Use `-` to indicate reverse order.
            project_id (:obj:`int`, optional): Numeric ID of the project containing jobs
        """
        return self._make_request(
            f'accounts/{account_id}/jobs/',
            params={'order_by': order_by, 'project_id': project_id},
        )

    def create_job(self, account_id: int, payload: Dict):
        """Return job details for a job on an account.

        Args:
            account_id (int): Numerc ID of the account containing the job
            job_id (int): Numeric ID of the job to retrieve
            order_by (:obj:`str`, optional): Field to order the result by.
                Use `-` to indicate reverse order.
        """
        return self._make_request(
            f'accounts/{account_id}/jobs/',
            method='post',
            json=payload,
        )

    def get_job(self, account_id: int, job_id: int, *, order_by: str = None):
        return self._make_request(
            f'accounts/{account_id}/jobs/{job_id}/',
            params={'order_by': order_by},
        )

    def update_job(self, account_id: int, job_id: int, payload: Dict):
        return self._make_request(
            f'accounts/{account_id}/jobs/{job_id}/',
            method='post',
            json=payload,
        )

    def trigger_job(self, account_id: int, job_id: int, payload: Dict):
        return self._make_request(
            f'accounts/{account_id}/jobs/{job_id}/run/',
            method='post',
            json=payload,
        )

    @staticmethod
    def _run_status_formatted(run_id: int, status: str, time: float) -> str:
        return f'Run {run_id} - {status.capitalize()}, Elapsed time: {round(time, 0)}s'

    def trigger_job_and_poll(
        self, account_id: int, job_id: int, payload: Dict, poll_interval: int = 10
    ) -> int:
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
        return self._make_request(
            f'accounts/{account_id}/runs',
            params={
                'include_related': include_related,
                'job_definition_id': job_definition_id,
                'order_by': order_by,
                'offset': offset,
                'limit': limit,
            },
        )

    def get_run(
        self, account_id: int, run_id: int, *, include_related: List[str] = None
    ):
        return self._make_request(
            f'accounts/{account_id}/runs/{run_id}',
            params={'include_related': include_related},
        )

    def list_run_artifacts(
        self,
        account_id: int,
        run_id: int,
        *,
        step: int = None,
    ):
        return self._make_request(
            f'accounts/{account_id}/runs/{run_id}/artifacts',
            params={'step': step},
        )

    def get_run_artifact(
        self,
        account_id: int,
        run_id: int,
        path: str,
        *,
        step: int = None,
    ):
        return self._make_request(
            f'accounts/{account_id}/runs/{run_id}/artifacts/{path}',
            params={'step': step},
        )

    def cancel_run(self, account_id: int, run_id: int):
        return self._make_request(
            f'accounts/{account_id}/runs/{run_id}/cancel',
            method='post',
        )

    def list_users(
        self,
        account_id: int,
        *,
        limit: int = None,
        offset: int = None,
        order_by: str = 'email',
    ):
        return self._make_request(
            f'accounts/{account_id}/users/',
            params={'limit': limit, 'offset': offset, 'order_by': order_by},
        )

    def list_invited_users(self, account_id: int):
        return self._make_request(f'accounts/{account_id}/invites/')

    def get_user(self, account_id: int, user_id: int):
        return self._make_request(f'accounts/{account_id}/users/{user_id}/')
