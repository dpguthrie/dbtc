# stdlib
from typing import Dict, List

from .base import _CloudClient


class _CloudClientV2(_CloudClient):
    def __init__(self, api_key: str = None):
        super().__init__(api_key=api_key)

    _base_url = 'https://cloud.getdbt.com/api/v2/'

    def list_accounts(self):
        return self._make_request('accounts')

    def get_account(self, account_id: int):
        return self._make_request(f'accounts/{account_id}')

    def list_projects(self, account_id: int):
        return self._make_request(f'accounts/{account_id}/projects')

    def get_project(self, account_id: int, project_id: int):
        return self._make_request(f'accounts/{account_id}/projects/{project_id}')

    def list_jobs(
        self, account_id: int, *, order_by: str = None, project_id: int = None
    ):
        return self._make_request(
            f'accounts/{account_id}/jobs',
            params={'order_by': order_by, 'project_id': project_id},
        )

    def create_job(self, account_id: int, payload: Dict):
        return self._make_request(
            f'accounts/{account_id}/jobs',
            method='POST',
            json=payload,
        )

    def get_job(self, account_id: int, job_id: int, *, order_by: str = None):
        return self._make_request(
            f'accounts/{account_id}/jobs/{job_id}',
            params={'order_by': order_by},
        )

    def update_job(self, account_id: int, job_id: int, payload: Dict):
        return self._make_request(
            f'accounts/{account_id}/jobs/{job_id}',
            method='POST',
            json=payload,
        )

    def trigger_job(self, account_id: int, job_id: int, payload: Dict):
        return self._make_request(
            f'accounts/{account_id}/jobs/{job_id}/run',
            method='POST',
            json=payload,
        )

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

    def get_run(self, account_id: int, run_id: int, *, include_related: List[str]):
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
            method='POST',
        )
