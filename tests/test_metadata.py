# stdlib
import datetime
from datetime import timedelta

# third party
import pytest

current_date = datetime.date.today()

# VARIABLES
START_DATE = (current_date - timedelta(weeks=2)).strftime("%Y-%m-%d")
END_DATE = (current_date - timedelta(days=1)).strftime("%Y-%m-%d")
JOB_ID = 73796
ACCOUNT_ID = 43786
ENVIRONMENT_ID = 218762
UNIQUE_ID = "model.tpch.dim_customers"
QUERY = """
query Environment($environmentId: BigInt!, $first: Int!, $after: String) {
    environment(id: $environmentId) {
        applied {
            models(first: $first, after: $after) {
                pageInfo {
                    startCursor
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                        uniqueId
                        executionInfo {
                            lastSuccessJobDefinitionId
                            lastSuccessRunId
                            executionTime
                        }
                    }
                }
            }
        }
    }
}
"""

PREDEFINED_METHODS = [
    "column_lineage",
    "longest_executed_models",
    "mesh_projects",
    "model_execution_history",
    "model_job_information",
    "most_executed_models",
    "most_failed_models",
    "most_models_test_failures",
    "public_models",
    "recommendations",
]


def _test_predefined_method(dbtc_client, method, *args, **kwargs):
    api = getattr(dbtc_client, "metadata")
    data = getattr(api, method)(*args, **kwargs)
    assert "data" in data
    assert "error" not in data


def test_query_no_variables(dbtc_client):
    query = f"{{models(jobId: {JOB_ID}) {{uniqueId}}}}"
    _test_predefined_method(dbtc_client, "query", query)


def test_query_with_variables(dbtc_client):
    query = "query GetMetadata($jobId: Int!) {models(jobId: $jobId) {uniqueId}}"
    variables = {"jobId": JOB_ID}
    _test_predefined_method(dbtc_client, "query", query, variables)


def test_pagination_combine_to_list(dbtc_client):
    variables = {"environmentId": ENVIRONMENT_ID, "first": 25, "after": None}
    data = dbtc_client.metadata.query(QUERY, variables, paginated_request_to_list=True)
    assert isinstance(data[0], dict)
    assert "node" in data[0]


def test_pagination_without_combining_lists(dbtc_client):
    variables = {"environmentId": ENVIRONMENT_ID, "first": 25, "after": None}
    data = dbtc_client.metadata.query(QUERY, variables)
    assert isinstance(data[0], dict)
    assert "data" in data[0]


def test_pagination_with_max_pages(dbtc_client):
    first = 10
    max_pages = 2
    variables = {"environmentId": ENVIRONMENT_ID, "first": first, "after": None}
    data = dbtc_client.metadata.query(
        QUERY, variables, max_pages=max_pages, paginated_request_to_list=True
    )
    assert isinstance(data[0], dict)
    assert len(data) == first * max_pages


def test_column_lineage(dbtc_client):
    _test_predefined_method(dbtc_client, "column_lineage", ENVIRONMENT_ID, UNIQUE_ID)


def test_longest_executed_models(dbtc_client):
    _test_predefined_method(
        dbtc_client,
        "longest_executed_models",
        ENVIRONMENT_ID,
        START_DATE,
        END_DATE,
    )


def test_mesh_projects(dbtc_client):
    _test_predefined_method(
        dbtc_client,
        "mesh_projects",
        ACCOUNT_ID,
    )


def test_model_execution_history(dbtc_client):
    _test_predefined_method(
        dbtc_client,
        "model_execution_history",
        ENVIRONMENT_ID,
        START_DATE,
        END_DATE,
        UNIQUE_ID,
    )


def test_model_job_information(dbtc_client):
    _test_predefined_method(
        dbtc_client,
        "model_job_information",
        ENVIRONMENT_ID,
        START_DATE,
        END_DATE,
        UNIQUE_ID,
    )


def test_most_executed_models(dbtc_client):
    _test_predefined_method(
        dbtc_client,
        "most_executed_models",
        ENVIRONMENT_ID,
        START_DATE,
        END_DATE,
        limit=25,
    )


def test_most_failed_models(dbtc_client):
    _test_predefined_method(
        dbtc_client,
        "most_failed_models",
        ENVIRONMENT_ID,
        START_DATE,
        END_DATE,
        limit=10,
    )


def test_most_models_test_failures(dbtc_client):
    _test_predefined_method(
        dbtc_client,
        "most_models_test_failures",
        ENVIRONMENT_ID,
        START_DATE,
        END_DATE,
        limit=2,
    )


def test_public_models(dbtc_client):
    _test_predefined_method(
        dbtc_client,
        "public_models",
        ACCOUNT_ID,
    )


def test_recommendations(dbtc_client):
    variables = {"environmentId": ENVIRONMENT_ID, "first": 500}
    data = dbtc_client.metadata.query(QUERY, variables)
    assert isinstance(data[0], dict)
    assert "data" in data[0]


def test_search(dbtc_client):
    data = dbtc_client.metadata.search(ENVIRONMENT_ID, "orders")
    assert "data" in data


def test_bad_search_access_level(dbtc_client):
    with pytest.raises(ValueError):
        dbtc_client.metadata.search(
            ENVIRONMENT_ID, "orders", access_level="super_private"
        )


def test_bad_search_resource_type(dbtc_client):
    with pytest.raises(ValueError):
        dbtc_client.metadata.search(ENVIRONMENT_ID, "orders", resource_type="modelino")


def test_bad_search_search_fields(dbtc_client):
    with pytest.raises(ValueError):
        dbtc_client.metadata.search(
            ENVIRONMENT_ID, "orders", search_fields=["secret_code"]
        )
