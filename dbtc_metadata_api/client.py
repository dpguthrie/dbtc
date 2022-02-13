# stdlib
import os
from typing import Dict, List

# third party
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

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

    def _get_python_field_names(self, obj: str, fields: List[str]):
        node = getattr(schema.Query, obj)
        return tuple((node._to_python_name(field)) for field in fields)

    def _make_request(
        self,
        obj: str,
        arguments: Dict = None,
        fields: List[str] = None,
        exclude: bool = False,
    ) -> Dict:
        op = Operation(schema.Query)
        instance = getattr(op, obj)(
            **{k: v for k, v in arguments.items() if v is not None}  # type: ignore
        )
        if fields is not None:
            fields = self._get_python_field_names(obj, fields)
            if exclude:
                instance.__fields__(__exclude__=fields)
            else:
                instance.__fields__(*fields)
        data = self._endpoint(op)
        return data

    def exposure(
        self,
        job_id: int,
        name: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "exposure",
            {"job_id": job_id, "name": name, "run_id": run_id},
            fields,
            exclude,
        )

    def exposures(
        self,
        job_id: int,
        name: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "exposures",
            {"job_id": job_id, "name": name, "run_id": run_id},
            fields,
            exclude,
        )

    def macro(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "macro",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
            exclude,
        )

    def macros(
        self,
        job_id: int,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "macros", {"job_id": job_id, "run_id": run_id}, fields, exclude
        )

    def metric(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "metric",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
            exclude,
        )

    def metrics(
        self,
        job_id: int,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "metric", {"job_id": job_id, "run_id": run_id}, fields, exclude
        )

    def model(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "model",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
            exclude,
        )

    def models(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
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
            exclude,
        )

    def seed(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "seed",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
            exclude,
        )

    def seeds(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "seeds",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
            exclude,
        )

    def snapshots(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
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
            exclude,
        )

    def source(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
    ) -> Dict:
        return self._make_request(
            "source",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
            exclude,
        )

    def sources(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
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
            exclude,
        )

    def test(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
        exclude: bool = False
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
        fields: List[str] = None,
        exclude: bool = False
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
            exclude,
        )
