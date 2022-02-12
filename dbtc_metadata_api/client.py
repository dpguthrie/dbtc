# stdlib
from typing import Dict, List, Tuple, Union
import operator
import os

# third party
from sgqlc.operation import Operation
from sgqlc.endpoint.http import HTTPEndpoint

# first party
from . import schema


class Client:
    def __init__(self, service_token: str = None) -> None:
        self.service_token = service_token or os.getenv("DBT_SERVICE_TOKEN")
        if self.service_token is None:
            raise ValueError(
                "A service token either must be provided or stored in the environment"
                ' variable "DBT_SERVICE_TOKEN"'
            )

    @property
    def url(self) -> str:
        return "https://metadata.cloud.getdbt.com/graphql"

    @property
    def headers(self) -> Dict[str, str]:
        return {"Authorization": "Bearer {}".format(self.service_token)}

    @property
    def _endpoint(self) -> HTTPEndpoint:
        return HTTPEndpoint(self.url, self.headers)

    def _make_request(
        self,
        resource: str,
        arguments: Dict = None,
        fields: List[str] = None,
    ) -> Dict:
        op = Operation(schema.Query)
        instance = getattr(op, resource)(
            **{k: v for k, v in arguments.items() if v is not None}
        )
        if fields is not None:
            for field in fields:
                if isinstance(field, str):
                    operator.attrgetter(field)(instance)()
                else:
                    operator.attrgetter(field[0])(instance)(**field[1])()
        data = self._endpoint(op)
        return data

    def exposure(
        self, job_id: int, name: str, *, run_id: int = None, fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "exposure", {"job_id": job_id, "name": name, "run_id": run_id}, fields
        )

    def exposures(
        self, job_id: int, name: str, *, run_id: int = None, fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "exposures", {"job_id": job_id, "name": name, "run_id": run_id}, fields
        )

    def macro(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "macro",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def macros(
        self, job_id: int, *, run_id: int = None, fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "macros", {"job_id": job_id, "run_id": run_id}, fields
        )

    def metric(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "metric",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def metrics(
        self, job_id: int, *, run_id: int = None, fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "metric", {"job_id": job_id, "run_id": run_id}, fields
        )

    def model(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "model",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def models(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
        fields: List[str] = None
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
            fields,
        )

    def seed(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "seed", {"job_id": job_id, "unique_id": unique_id, "run_id": run_id}, fields
        )

    def seeds(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "seeds",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def snapshots(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
        fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "snapshots",
            {
                "job_id": job_id,
                "database": database,
                "schema": schema,
                "identifier": identifier,
                "run_id": run_id,
            },
            fields,
        )

    def source(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "source",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def sources(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
        fields: List[str] = None
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
            fields,
        )

    def test(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "test", {"job_id": job_id, "unique_id": unique_id, "run_id": run_id}, fields
        )

    def tests(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
        fields: List[str] = None
    ) -> Dict:
        return self._make_request(
            "tests",
            {
                "job_id": job_id,
                "database": database,
                "schema": schema,
                "identifier": identifier,
                "run_id": run_id,
            },
            fields,
        )
