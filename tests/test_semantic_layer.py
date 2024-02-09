# third party
import pandas as pd
import pyarrow as pa
import pytest

# first party
from dbtc.models.semantic_layer import QueryResponse


def test_bad_output_format(dbtc_client):
    with pytest.raises(ValueError):
        dbtc_client.sl.query(metrics=["total_revenue"], output_format="dict")


def test_only_metrics(dbtc_client):
    response = dbtc_client.sl.query(metrics=["total_revenue"])
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, pd.DataFrame)
    assert "TOTAL_REVENUE" in response.result.columns


def test_metrics_and_group_by(dbtc_client):
    response = dbtc_client.sl.query(metrics=["total_revenue"], group_by=["metric_time"])
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, pd.DataFrame)
    assert "TOTAL_REVENUE" in response.result.columns
    assert "METRIC_TIME__DAY" in response.result.columns


def test_different_grain(dbtc_client):
    response = dbtc_client.sl.query(
        metrics=["total_revenue"], group_by=["metric_time"], grain="month"
    )
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, pd.DataFrame)
    assert "TOTAL_REVENUE" in response.result.columns
    assert "METRIC_TIME__MONTH" in response.result.columns


def test_multiple_group_by_types(dbtc_client):
    response = dbtc_client.sl.query(
        metrics=["total_revenue"],
        group_by=["metric_time", {"name": "metric_time", "grain": "month"}],
    )
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, pd.DataFrame)
    assert "TOTAL_REVENUE" in response.result.columns
    assert "METRIC_TIME__MONTH" in response.result.columns


def test_bad_order_by(dbtc_client):
    with pytest.raises(ValueError):
        dbtc_client.sl.query(
            metrics=["total_revenue", "total_profit"],
            group_by=[
                "customer__nation",
                "customer__region",
                {"name": "metric_time", "date_part": "month"},
            ],
            limit=5,
            order_by=["customer_region", {"name": "total_revenue", "desc": True}],
        )


def test_all_args(dbtc_client):
    response = dbtc_client.sl.query(
        metrics=["total_revenue", "total_profit"],
        group_by=[
            "customer__nation",
            "customer__region",
            {"name": "metric_time", "date_part": "month"},
        ],
        limit=5,
        order_by=["customer__region", {"name": "total_revenue", "desc": True}],
    )
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, pd.DataFrame)
    assert "CUSTOMER__NATION" in response.result.columns
    assert "CUSTOMER__REGION" in response.result.columns
    assert len(response.result) == 5


def test_bad_metric(dbtc_client):
    response = dbtc_client.sl.query(metrics=["bad_metric"])
    assert isinstance(response, QueryResponse)
    assert response.result is None
    assert response.error is not None
    assert response.sql is None


def test_bad_group_by(dbtc_client):
    response = dbtc_client.sl.query(
        metrics=["total_revenue"], group_by=["bad_group_by"]
    )
    assert isinstance(response, QueryResponse)
    assert response.result is None
    assert response.error is not None
    assert response.sql is None


def test_bad_limit(dbtc_client):
    response = dbtc_client.sl.query(metrics=["total_revenue"], limit=-1)
    assert isinstance(response, QueryResponse)
    assert response.result is None
    assert response.sql is None
    assert response.error is not None


def test_saved_metric(dbtc_client):
    response = dbtc_client.sl.query(saved_query="sales_metrics")
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, pd.DataFrame)


def test_saved_metric_with_limit(dbtc_client):
    response = dbtc_client.sl.query(saved_query="sales_metrics", limit=7)
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, pd.DataFrame)
    assert len(response.result) == 7


def test_list_output_format(dbtc_client):
    response = dbtc_client.sl.query(metrics=["total_revenue"], output_format="list")
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, list)
    assert isinstance(response.result[0], dict)


def test_raw_output_format(dbtc_client):
    response = dbtc_client.sl.query(metrics=["total_revenue"], output_format="raw")
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, list)
    assert isinstance(response.result[0], str)


def test_arrow_output_format(dbtc_client):
    response = dbtc_client.sl.query(metrics=["total_revenue"], output_format="arrow")
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, pa.Table)


def test_list_dimensions(dbtc_client):
    response = dbtc_client.sl.list_dimensions(metrics=["total_revenue"])
    assert isinstance(response, dict)
    assert "data" in response
    assert "dimensions" in response.get("data", {})


def test_list_entities(dbtc_client):
    response = dbtc_client.sl.list_entities(metrics=["total_revenue"])
    assert isinstance(response, dict)
    assert "data" in response
    assert "entities" in response.get("data", {})


def test_list_measures(dbtc_client):
    response = dbtc_client.sl.list_measures(metrics=["total_revenue"])
    assert isinstance(response, dict)
    assert "data" in response
    assert "measures" in response.get("data", {})


def test_list_metrics(dbtc_client):
    response = dbtc_client.sl.list_metrics()
    assert isinstance(response, dict)
    assert "data" in response
    assert "metrics" in response.get("data", {})


def test_metrics_for_dimensions(dbtc_client):
    response = dbtc_client.sl.list_metrics_for_dimensions(
        dimensions=["customer__nation"]
    )
    assert isinstance(response, dict)
    assert "data" in response
    assert "metricsForDimensions" in response.get("data", {})


def test_queryable_granularities(dbtc_client):
    response = dbtc_client.sl.list_queryable_granularities(["total_revenue"])
    assert isinstance(response, dict)
    assert "data" in response
    assert "queryableGranularities" in response.get("data", {})


def test_saved_queries(dbtc_client):
    response = dbtc_client.sl.list_saved_queries()
    assert isinstance(response, dict)
    assert "data" in response
    assert "savedQueries" in response.get("data", {})


def test_dimension_values(dbtc_client):
    response = dbtc_client.sl.list_dimension_values(group_by=["customer__region"])
    assert isinstance(response, QueryResponse)
    assert isinstance(response.result, pd.DataFrame)
    assert "CUSTOMER__REGION" in response.result.columns
