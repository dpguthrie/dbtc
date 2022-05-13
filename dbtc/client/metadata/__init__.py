# stdlib
from typing import Dict

# third party
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

# first party
from dbtc.client.base import _Client
from dbtc.client.metadata.schema import Query


class _MetadataClient(_Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    _header_property = 'service_token'
    _default_domain = 'metadata.cloud.getdbt.com'
    _path = '/graphql'

    @property
    def _endpoint(self) -> HTTPEndpoint:
        return HTTPEndpoint(self.full_url(), self.headers)

    def _make_request(self, obj: str, arguments: Dict = None) -> Dict:
        op = Operation(Query)
        getattr(op, obj)(  # noqa: F841
            **{k: v for k, v in arguments.items() if v is not None}  # type: ignore
        ).__fields__()
        data = self._endpoint(op)
        return data

    def get_exposure(self, job_id: int, name: str, *, run_id: int = None) -> Dict:
        return self._make_request(
            "exposure",
            {"job_id": job_id, "name": name, "run_id": run_id},
        )

    def get_exposures(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "exposures",
            {"job_id": job_id, "run_id": run_id},
        )

    def get_macro(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "macro",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_macros(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request("macros", {"job_id": job_id, "run_id": run_id})

    def get_metric(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "metric",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_metrics(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request("metrics", {"job_id": job_id, "run_id": run_id})

    def get_model(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "model",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_models(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "models",
            {
                "job_id": job_id,
                "database": database,
                "schema": schema,
                "identifier": identifier,
                "run_id": run_id,
            },
        )

    def get_seed(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "seed",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_seeds(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "seeds",
            {"job_id": job_id, "run_id": run_id},
        )

    def get_snapshot(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "snapshot",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_snapshots(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "snapshots",
            {
                "job_id": job_id,
                "run_id": run_id,
            },
        )

    def get_source(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "source",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
        )

    def get_sources(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "sources",
            {
                "job_id": job_id,
                "database": database,
                "schema": schema,
                "identifier": identifier,
                "run_id": run_id,
            },
        )

    def get_test(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "test", {"job_id": job_id, "unique_id": unique_id, "run_id": run_id}
        )

    def get_tests(
        self,
        job_id: int,
        *,
        run_id: int = None,
    ) -> Dict:
        return self._make_request(
            "tests",
            {
                "job_id": job_id,
                "run_id": run_id,
            },
        )
