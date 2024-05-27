# stdlib
from enum import Enum
from typing import Dict, List, Optional, Union

# first party
from dbtc.client.base import _Client
from dbtc.models import semantic_layer as sl_models

MULTI_TENANT_HOSTS = [
    "cloud.getdbt.com",
    "emea.dbt.com",
    "au.dbt.com",
]


class OutputFormatType(Enum):
    PANDAS = "pandas"
    ARROW = "arrow"
    LIST = "list"
    RAW = "raw"


class _SemanticLayerClient(_Client):
    QUERIES = {
        "entities": """
query GetEntities($environmentId: BigInt!, $metrics: [MetricInput!]!) {
  entities(environmentId: $environmentId, metrics: $metrics) {
    description
    expr
    name
    role
    type
  }
}
        """,
        "saved_queries": """
query GetSavedQueries($environmentId: BigInt!) {
  savedQueries(environmentId: $environmentId) {
    description
    label
    metadata {
      repoFilePath
      fileSlice {
        content
        endLineNumber
        filename
        startLineNumber
      }
    }
    name
    queryParams {
      groupBy {
        datePart
        grain
        name
      }
      metrics {
        name
      }
      where {
        whereSqlTemplate
      }
    }
  }
}
        """,
        "metrics": """
query GetMetrics($environmentId: BigInt!) {
    metrics(environmentId: $environmentId) {
        description
        requiresMetricTime
        measures {
            agg
            aggTimeDimension
            expr
            name
        }
        entities {
            description
            expr
            name
            role
            type
        }
        filter {
            whereSqlTemplate
        }
        label
        name
        queryableGranularities
        type
        typeParams {
            denominator {
                alias
                filter {
                    whereSqlTemplate
                }
                name
                offsetToGrain
                offsetWindow {
                    count
                    granularity
                }
            }
            expr
            grainToDate
            inputMeasures {
                alias
                filter {
                    whereSqlTemplate
                }
                name
            }
            measure {
                alias
                filter {
                    whereSqlTemplate
                }
                name
            }
            metrics {
                alias
                filter {
                    whereSqlTemplate
                }
                name
                offsetToGrain
                offsetWindow {
                    count
                    granularity
                }
            }
            numerator {
                alias
                filter {
                    whereSqlTemplate
                }
                name
                offsetToGrain
                offsetWindow {
                    count
                    granularity
                }
            }
            window {
                count
                granularity
            }
        }
        dimensions {
            description
            expr
            isPartition
            label
            name
            qualifiedName
            queryableGranularities
            type
            typeParams {
                timeGranularity
                validityParams {
                    isEnd
                    isStart
                }
            }
        }
    }
}
        """,
        "dimensions": """
query GetDimensions($environmentId: BigInt!, $metrics: [MetricInput!]!) {
    dimensions(environmentId: $environmentId, metrics: $metrics) {
        description
        expr
        isPartition
        metadata {
        fileSlice {
            content
            endLineNumber
            filename
            startLineNumber
        }
        repoFilePath
        }
        name
        qualifiedName
        type
        typeParams {
        timeGranularity
        validityParams {
            isEnd
            isStart
        }
        }
    }
}
        """,
        "dimension_values": """
mutation GetDimensionValues($environmentId: BigInt!, $groupBy: [GroupByInput!]!, $metrics: [MetricInput!]!) {
    createDimensionValuesQuery(
        environmentId: $environmentId
        groupBy: $groupBy
        metrics: $metrics
    ) {
        queryId
    }
}
        """,
        "metric_for_dimensions": """
query GetMetricsForDimensions($environmentId: BigInt!, $dimensions: [GroupByInput!]) {
    metricsForDimensions(environmentId: $environmentId, dimensions: $dimensions) {
        description
        name
        queryableGranularities
        type
    }
}
        """,
        "create_query": """
mutation CreateQuery($groupBy: [GroupByInput!], $limit: Int, $metrics: [MetricInput!], $orderBy: [OrderByInput!], $savedQuery: String, $where: [WhereInput!], $environmentId: BigInt!) {
  createQuery(
    environmentId: $environmentId
    limit: $limit
    metrics: $metrics
    savedQuery: $savedQuery
    where: $where
    groupBy: $groupBy
    orderBy: $orderBy
  ) {
    queryId
  }
}
        """,
        "dimension_values_query": """
mutation CreateDimensionValuesQuery($groupBy: [GroupByInput!]!, $metrics: [MetricInput!]!, $environmentId: BigInt!) {
  createDimensionValuesQuery(
    environmentId: $environmentId
    groupBy: $groupBy
    metrics: $metrics
  ) {
    queryId
  }
}
        """,
        "get_results": """
query GetResults($pageNum: Int, $environmentId: BigInt!, $queryId: String!) {
  query(environmentId: $environmentId, queryId: $queryId, pageNum: $pageNum) {
    arrowResult
    error
    queryId
    sql
    status
    totalPages
  }
}
        """,
        "queryable_granularities": """
query GetQueryableGranularities($environmentId: BigInt!, $metrics:[MetricInput!]!) {
    queryableGranularities(environmentId: $environmentId, metrics: $metrics)
}
        """,
        "metrics_for_dimensions": """
query GetMetricsForDimensions($environmentId: BigInt!, $dimensions:[GroupByInput!]!) {
    metricsForDimensions(environmentId: $environmentId, dimensions: $dimensions) {
        description
        name
        queryableGranularities
        type
        filter {
            whereSqlTemplate
        }
    }
}
        """,
        "measures": """
query GetMeasures($environmentId: BigInt!, $metrics: [MetricInput!]!) {
  measures(environmentId: $environmentId, metrics: $metrics) {
    agg
    aggTimeDimension
    expr
    name
  }
}
        """,
    }

    def __init__(self, session, **kwargs):
        super().__init__(session, **kwargs)

    _header_property = "service_token"

    @property
    def _path(self):
        return "/api/graphql"

    @property
    def _base_url(self):
        if self._host in MULTI_TENANT_HOSTS:
            return f"https://semantic-layer.{self._host}{self._path}"

        return f"https://{self.host}.semantic-layer{self._path}"

    def _convert_to_metric_input(self, metrics: List[str]) -> List[Dict]:
        return [sl_models.MetricInput(name=metric).model_dump() for metric in metrics]

    def _convert_to_groupby_input(
        self, dimensions: List[Union[str, Dict[str, Optional[str]]]], grain: str = None
    ) -> List[Dict]:
        groupby_inputs = []
        for dimension in dimensions:
            fields = {}
            if isinstance(dimension, str):
                if dimension == "metric_time":
                    fields["grain"] = grain
                fields["name"] = dimension
            else:
                fields = dimension
            groupby_inputs.append(
                sl_models.GroupByInput(**fields).model_dump(exclude_none=True)
            )
        return groupby_inputs

    def _convert_to_orderby_input(
        self,
        order_by_list: List[Union[str, Dict[str, Optional[str]]]],
        metric_inputs: List[Dict],
        groupby_inputs: List[Dict],
    ) -> List[Dict]:
        def get_input(
            input_type: str, name: str, inputs: List[Dict], descending: bool = False
        ):
            try:
                item = [m for m in inputs if m["name"] == name][0]

            except IndexError:
                return None

            return sl_models.OrderByInput(
                **{input_type: item, "descending": descending}
            ).model_dump()

        def get_metric_input(
            name: str, metric_inputs: List[Dict], descending: bool = False
        ):
            return get_input("metric", name, metric_inputs, descending)

        def get_groupby_input(
            name: str, groupby_inputs: List[Dict], descending: bool = False
        ):
            return get_input("groupBy", name, groupby_inputs, descending)

        def get_either_input(
            name: str,
            metric_inputs: List[Dict],
            group_by_inputs: List[Dict],
            descending: bool = False,
        ):
            metric_input = get_metric_input(name, metric_inputs, descending)
            if metric_input is not None:
                return metric_input

            group_by_input = get_groupby_input(name, group_by_inputs, descending)
            if group_by_input is not None:
                return group_by_input

            raise ValueError(
                f"Could not find {name} in either metric or groupBy inputs"
            )

        order_by_inputs = []
        for order_by in order_by_list:
            if isinstance(order_by, str):
                order_by_inputs.append(
                    get_either_input(order_by, metric_inputs, groupby_inputs)
                )
            else:
                order_by_inputs.append(
                    get_either_input(
                        order_by["name"],
                        metric_inputs,
                        groupby_inputs,
                        order_by.get("descending", order_by.get("desc", False)),
                    )
                )
        return order_by_inputs

    def _get_query_response(
        self, payload: Dict, response_key: str, output_format: str
    ) -> sl_models.QueryResponse:
        json_response = self.make_request(payload)
        try:
            query_id = json_response["data"][response_key]["queryId"]
        except TypeError:
            error = json_response["errors"][0]["message"]
            raise ValueError(error)

        results_payload = {
            "query": self.QUERIES["get_results"],
            "variables": {
                "queryId": query_id,
                "pageNum": 1,
            },
        }
        query_pages_list = self._poll_for_results(results_payload)
        query_response = sl_models.QueryResponseConstructor(
            query_pages_list, output_format
        ).create()
        return query_response

    def _poll_for_results(self, payload: Dict) -> List[sl_models.QueryResponse]:
        responses = []
        while True:
            json_response = self.make_request(payload)
            try:
                data = json_response["data"]["query"]
            except TypeError:
                error = json_response["errors"][0]["message"]
                raise ValueError(error)
            else:
                status = data["status"].lower()
                if status in ["successful", "failed"]:
                    responses.append(sl_models.QueryPage(**data))
                    if (
                        data["totalPages"]
                        and data["totalPages"] > payload["variables"]["pageNum"]
                    ):
                        payload["variables"]["pageNum"] += 1
                    else:
                        break

        return responses

    def make_request(self, payload: Dict) -> Dict:
        if "variables" not in payload:
            payload["variables"] = {}
        payload["variables"]["environmentId"] = self.environment_id
        response = self.session.post(self.full_url(), json=payload)
        response.raise_for_status()
        return response.json()

    def list_dimensions(self, metrics: List[str]) -> Dict:
        return self.make_request(
            {
                "query": self.QUERIES["dimensions"],
                "variables": {"metrics": self._convert_to_metric_input(metrics)},
            }
        )

    def list_entities(self, metrics: List[str]) -> Dict:
        return self.make_request(
            {
                "query": self.QUERIES["entities"],
                "variables": {"metrics": self._convert_to_metric_input(metrics)},
            }
        )

    def list_measures(self, metrics: List[str]) -> Dict:
        metric_input = self._convert_to_metric_input(metrics)
        return self.make_request(
            {
                "query": self.QUERIES["measures"],
                "variables": {"metrics": metric_input},
            }
        )

    def list_metrics(self) -> Dict:
        return self.make_request({"query": self.QUERIES["metrics"]})

    def list_metrics_for_dimensions(
        self, dimensions: List[Union[str, Dict[str, str]]]
    ) -> Dict:
        return self.make_request(
            {
                "query": self.QUERIES["metrics_for_dimensions"],
                "variables": {"dimensions": self._convert_to_groupby_input(dimensions)},
            }
        )

    def list_queryable_granularities(self, metrics: List[str]) -> Dict:
        return self.make_request(
            {
                "query": self.QUERIES["queryable_granularities"],
                "variables": {"metrics": self._convert_to_metric_input(metrics)},
            }
        )

    def list_saved_queries(self):
        return self.make_request({"query": self.QUERIES["saved_queries"]})

    def list_dimension_values(
        self,
        *,
        metrics: List[str] = None,
        group_by: List[Union[str, Dict[str, str]]] = None,
        output_format: str = OutputFormatType.PANDAS.value,
    ):
        if metrics is None and group_by is None:
            raise ValueError("either metrics or groupBy is required")

        variables = {
            "metrics": self._convert_to_metric_input(metrics) if metrics else [],
            "groupBy": self._convert_to_groupby_input(group_by) if group_by else [],
        }
        payload = {
            "query": self.QUERIES["dimension_values_query"],
            "variables": variables,
        }
        return self._get_query_response(
            payload, "createDimensionValuesQuery", output_format
        )

    def query(
        self,
        *,
        metrics: List[str] = None,
        group_by: List[Union[str, Dict[str, Optional[str]]]] = None,
        limit: int = None,
        where: str = None,
        order_by: List[Union[str, Dict[str, Optional[str]]]] = None,
        saved_query: str = None,
        grain: str = "DAY",
        output_format: str = OutputFormatType.PANDAS.value,
    ):
        # Check output format
        is_valid_output_format = output_format in (
            item.value for item in OutputFormatType
        )
        if not is_valid_output_format:
            raise ValueError(f"Invalid output_format: {output_format}")

        # Initialize variables
        metric_inputs = self._convert_to_metric_input(metrics) if metrics else []
        group_by_inputs = (
            self._convert_to_groupby_input(group_by, grain) if group_by else []
        )
        order_by_inputs = (
            self._convert_to_orderby_input(order_by, metric_inputs, group_by_inputs)
            if order_by
            else []
        )

        variables = {
            "metrics": metric_inputs,
            "groupBy": group_by_inputs,
            "limit": limit,
            "where": where,
            "savedQuery": saved_query,
            "orderBy": order_by_inputs,
        }

        payload = {"query": self.QUERIES["create_query"], "variables": variables}
        return self._get_query_response(payload, "createQuery", output_format)
