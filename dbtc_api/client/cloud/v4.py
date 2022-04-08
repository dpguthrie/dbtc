# stdlib
from typing import Dict, List

# first party
from dbtc_api.client.cloud.base import _CloudClient


class _CloudClientV4(_CloudClient):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.limit = kwargs.get('limit', 100)
        self.max_records = kwargs.get('max_records', None)

    _default_domain = 'cloud.getdbt.com'
    _path = '/api/v4/'

    def _get_pagination_token(self, response):
        return response.headers.get('x-dbt-continuation-token', None)

    def _make_request(self, path: str, *, method: str = 'get', **kwargs):
        full_url = self.full_url(path)
        response = self.session.request(method, full_url, **kwargs)
        return response

    def _paginated_request(
        self, path: str, *, method: str = 'get', **kwargs
    ) -> List[Dict]:
        data = []
        response = self._make_request(path, method=method, **kwargs)
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

    def list_runs(
        self,
        account_id: int,
        *,
        limit: int = None,
        environment: str = None,
        project: str = None,
        job: str = None,
        status: str = None,
    ) -> List[Dict]:
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

    def get_run(self, account_id: int, run_id: int) -> Dict:
        return self._paginated_request(f'accounts/{account_id}/runs/{run_id}')[0]
