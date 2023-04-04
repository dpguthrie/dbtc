# stdlib
import operator
from typing import Any, Dict, List

# third party
import requests
from sgqlc.endpoint.http import HTTPEndpoint
from sgqlc.operation import Operation

# first party
from dbtc.client.base import _Client
from dbtc.client.schema import Query
from dbtc.utils import camel_to_snake


class _MetadataClient(_Client):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.session = requests.Session()
        self.session.headers = self.headers

    _header_property = 'service_token'
    _path = '/graphql'

    @property
    def _base_url(self):
        return f'https://metadata.{self._host}{self._path}'

    @property
    def _endpoint(self) -> HTTPEndpoint:
        return HTTPEndpoint(self.full_url(), self.headers)

    def _get_nested_field(self, nested_field: List[str], field_dict: Dict):
        value = nested_field[-1]
        key = '.'.join(nested_field[:-1])
        if key not in field_dict:
            field_dict[key] = []
        field_dict[key].append(value)
        return field_dict

    def _get_field_dict(self, fields: List[str]):
        field_dict: Dict = {'top_level': []}
        for field in fields:
            nested_field = [camel_to_snake(f) for f in field.split('.')]
            if len(nested_field) == 1:
                field_dict['top_level'].append(nested_field[0])
            else:
                field_dict = self._get_nested_field(nested_field, field_dict)
        return field_dict

    def _make_request(
        self, obj: str, arguments: Dict = None, fields: List[str] = None
    ) -> Dict:
        op = Operation(Query)
        arguments = {
            k: v for k, v in arguments.items() if v is not None  # type: ignore
        }
        if fields is not None:
            query = getattr(op, obj)(**arguments)
            field_dict = self._get_field_dict(fields)
            for k, v in field_dict.items():
                if k == 'top_level':
                    query.__fields__(*v)
                else:
                    operator.attrgetter(k)(query).__fields__(*v)
        else:
            getattr(op, obj)(**arguments).__fields__()
        data = self._endpoint(op)
        if not self.do_not_track:
            arguments['fields'] = fields
            self._send_track(
                'Metadata API',
                getattr(self, f'get_{obj}'),
                **arguments,
            )
        return data

    def query(self, query: str, variables: Dict = None):
        payload: Dict[str, Any] = {'query': query}
        if variables:
            payload.update({'variables': variables})
        response = self.session.post(self.full_url(), json=payload)
        return response.json()

    def get_exposure(
        self, job_id: int, name: str, *, run_id: int = None, fields: List[str] = None
    ) -> Dict:
        """
        The exposure object allows you to query information about a particular
            exposure. You can learn more about exposures [here](
            https://docs.getdbt.com/docs/building-a-dbt-project/exposures).

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this expsoure was
                generated for
            name (str): The name of this particular exposure
            run_id (int, optional): The run ID of the run in dbt Cloud that this
                exposure was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "exposure",
            {"job_id": job_id, "name": name, "run_id": run_id},
            fields,
        )

    def get_exposures(
        self,
        job_id: int,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The exposures object allows you to query information about all exposures in a
            given job. You can learn more about exposures [here](
            https://docs.getdbt.com/docs/building-a-dbt-project/exposures).

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this exposure was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this
                exposure was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "exposures",
            {"job_id": job_id, "run_id": run_id},
            fields,
        )

    def get_macro(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The macro object allows you to query information about a particular macro in a
        given job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this macro was
                generated for
            unique_id (str): The unique ID of this particular macro
            run_id (int, optional): The run ID of the run in dbt Cloud that this macro
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "macro",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def get_macros(
        self,
        job_id: int,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The macros object allows you to query information about all macros in a
            given job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this macro was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this macro
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "macros", {"job_id": job_id, "run_id": run_id}, fields
        )

    def get_metric(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The metric object allows you to query information about [metrics](
            https://docs.getdbt.com/docs/building-a-dbt-project/metrics).

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this metric was
                generated for
            unique_id (str): The unique ID of this particular metric
            run_id (int, optional): The run ID of the run in dbt Cloud that this metric
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "metric",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def get_metrics(
        self,
        job_id: int,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The metrics object allows you to query information about [metrics](
            https://docs.getdbt.com/docs/building-a-dbt-project/metrics).

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this metric was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this metric
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "metrics", {"job_id": job_id, "run_id": run_id}, fields
        )

    def get_model(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The model object allows you to query information about a particular model in a
        given job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            unique_id (str): The unique ID of this particular model
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "model",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def get_model_by_environment(
        self,
        environment_id: int,
        unique_id: str,
        last_run_count: int = 10,
        with_catalog: bool = False,
        fields: List[str] = None,
    ):
        """The model by environment object allows you to query information about a
        particular model based on environment_id

        !!! warning
            This feature is currently in beta and subject to change.

        Args:
            environment_id (int): The environment_id for this model
            unique_id (str): The unique ID of this model
            last_run_count (int, optional): Number of last run results where this model
                was built to return (max of 10). Defaults to 10.
            with_catalog (bool, optional): If true, return only runs that have catalog
                information for this model. Defaults to False.
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "model_by_environment",
            {
                "environment_id": environment_id,
                "unique_id": unique_id,
                "last_run_count": last_run_count,
                "with_catalog": with_catalog,
            },
            fields,
        )

    def get_models(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The models object allows you to query information about all models in a given
            job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this model was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this model
                was generated for
            database (str, optional): The database where this table/view lives
            schema (str, optional): The schema where this table/view lives
            identifier (str, optional): The identifier of this table/view
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
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

    def get_seed(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The seed object allows you to query information about a particular seed in a
            given job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this seed was
                generated for
            unique_id (str): The unique ID of this particular seed
            run_id (int, optional): The run ID of the run in dbt Cloud that this seed
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "seed", {"job_id": job_id, "unique_id": unique_id, "run_id": run_id}, fields
        )

    def get_seeds(
        self,
        job_id: int,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The seeds object allows you to query information about a all seeds in a given
            job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this seed was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this seed
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request("seeds", {"job_id": job_id, "run_id": run_id}, fields)

    def get_snapshot(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The snapshot object allows you to query information about a particular
            snapshot.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this snapshot was
                generated for
            unique_id (str): The unique ID of this particular snapshot
            run_id (int, optional): The run ID of the run in dbt Cloud that this
                snapshot was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "snapshot",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def get_snapshots(
        self,
        job_id: int,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The snapshots object allows you to query information about all snapshots in a
            given job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this snapshot was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this
                snapshot was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.

        """
        return self._make_request(
            "snapshots",
            {
                "job_id": job_id,
                "run_id": run_id,
            },
            fields,
        )

    def get_source(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The source object allows you to query information about a particular source in
            a given job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this source was
                generated for
            unique_id (str): The unique ID of this particular source
            run_id (int, optional): The run ID of the run in dbt Cloud that this source
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "source",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def get_sources(
        self,
        job_id: int,
        *,
        database: str = None,
        schema: str = None,
        identifier: str = None,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The snapshots object allows you to query information about all snapshots in a
            given job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this source was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this source
                was generated for
            database (str, optional): The database where this table/view lives
            schema (str, optional): The schema where this table/view lives
            identifier (str, optional): The identifier of this table/view
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
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

    def get_test(
        self,
        job_id: int,
        unique_id: str,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The test object allows you to query information about a particular test.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this test was
                generated for
            unique_id (str): The unique ID of this particular test
            run_id (int, optional): The run ID of the run in dbt Cloud that this test
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "test",
            {"job_id": job_id, "unique_id": unique_id, "run_id": run_id},
            fields,
        )

    def get_tests(
        self,
        job_id: int,
        *,
        run_id: int = None,
        fields: List[str] = None,
    ) -> Dict:
        """
        The tests object allows you to query information about all tests in a given
            job.

        Args:
            job_id (int): The unique ID of the job in dbt Cloud that this test was
                generated for
            run_id (int, optional): The run ID of the run in dbt Cloud that this test
                was generated for
            fields (list, optional): The list of fields to include in the response.
                The field can either be in snake_case or camelCase (e.g. run_id and
                runId will be evaluated similarly).  Nested fields can be accessed
                with a `.` (e.g. `parentsSources.criteria.warnAfter.errorAfter`)

        !!! note
            If you do not include a run_id, it will default to the most recent run of
            the specified job.
        """
        return self._make_request(
            "tests",
            {
                "job_id": job_id,
                "run_id": run_id,
            },
            fields,
        )
