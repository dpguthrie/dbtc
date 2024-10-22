# third party
import pytest

ACCOUNT_ID = 43786
PROJECT_ID = 146088
JOB_ID = 229335


def _test_cloud_method(dbtc_client, method: str, **kwargs):
    "Assert that response status code is 200"
    data = getattr(dbtc_client.cloud, method)(account_id=ACCOUNT_ID, **kwargs)
    assert data["status"]["code"] == 200


def _test_and_set(dbtc_client, method: str, variable: str, **kwargs):
    response = getattr(dbtc_client.cloud, method)(**kwargs)
    data = response["data"]
    if isinstance(data, list):
        setattr(pytest, variable, data[0]["id"])
    else:
        setattr(pytest, variable, data["id"])
    assert True


@pytest.mark.dependency()
def test_no_access(dbtc_client):
    try:
        response = dbtc_client.cloud.list_projects(account_id=0)
        response["data"][0]["id"]
    except TypeError:
        assert response["status"]["code"] == 404


@pytest.mark.dependency()
def test_list_accounts(dbtc_client):
    data = dbtc_client.cloud.list_accounts()
    assert data["status"]["code"] == 200


@pytest.mark.dependency(depends=["test_list_accounts"])
def test_get_account(dbtc_client):
    _test_cloud_method(dbtc_client, "get_account")


@pytest.mark.dependency(depends=["test_list_accounts"])
def test_get_account_by_name(dbtc_client):
    accounts = dbtc_client.cloud.list_accounts()
    account_name = accounts["data"][0]["name"]
    data = dbtc_client.cloud.get_account_by_name(account_name)
    assert data["status"]["code"] == 200


@pytest.mark.dependency(depends=["test_list_accounts"])
def test_bad_get_account_by_name(dbtc_client):
    with pytest.raises(Exception):
        dbtc_client.cloud.get_account_by_name("Bad Account Name")


@pytest.mark.dependency(depends=["test_list_accounts"])
def test_get_account_licenses(dbtc_client):
    _test_cloud_method(dbtc_client, "get_account_licenses")


@pytest.mark.dependency(depends=["test_list_accounts"])
def test_list_invited_users(dbtc_client):
    _test_cloud_method(dbtc_client, "list_invited_users")


@pytest.mark.dependency(depends=["test_list_accounts"])
def test_list_environments_by_account(dbtc_client):
    _test_cloud_method(dbtc_client, "list_environments", project_id=PROJECT_ID)


@pytest.mark.dependency(depends=["test_list_accounts"])
def test_list_projects(dbtc_client):
    _test_cloud_method(dbtc_client, "list_projects")


@pytest.mark.dependency(depends=["test_list_projects"])
def test_list_users(dbtc_client):
    _test_and_set(dbtc_client, "list_users", "user_id", account_id=ACCOUNT_ID)


@pytest.mark.dependency(depends=["test_list_projects"])
def test_list_environments_by_project(dbtc_client):
    _test_cloud_method(dbtc_client, "list_environments", project_id=PROJECT_ID)


@pytest.mark.dependency(depends=["test_list_projects"])
def test_get_project(dbtc_client):
    _test_cloud_method(dbtc_client, "get_project", project_id=PROJECT_ID)


@pytest.mark.dependency(depends=["test_list_projects"])
def test_get_project_by_name(dbtc_client):
    projects = dbtc_client.cloud.list_projects(ACCOUNT_ID)
    project_name = projects["data"][0]["name"]
    data = dbtc_client.cloud.get_project_by_name(project_name)
    assert data["status"]["code"] == 200


@pytest.mark.dependency(depends=["test_list_projects"])
def test_get_bad_project_by_name(dbtc_client):
    with pytest.raises(Exception):
        dbtc_client.cloud.get_project_by_name("Bad Project Name", account_id=ACCOUNT_ID)


@pytest.mark.dependency(depends=["test_list_projects"])
def test_get_bad_project_by_name_2(dbtc_client):
    with pytest.raises(Exception):
        dbtc_client.cloud.get_project_by_name("Bad Project Name", account_id=ACCOUNT_ID)


@pytest.mark.dependency(depends=["test_list_users"])
def test_get_user(dbtc_client):
    _test_cloud_method(dbtc_client, "get_user", user_id=pytest.user_id)


@pytest.mark.dependency(depends=["test_list_projects"])
def test_list_jobs(dbtc_client):
    _test_cloud_method(dbtc_client, "list_jobs")


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_get_job(dbtc_client):
    _test_cloud_method(dbtc_client, "get_job", job_id=JOB_ID)


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs(dbtc_client):
    _test_and_set(
        dbtc_client,
        "list_runs",
        "run_id",
        account_id=ACCOUNT_ID,
        job_definition_id=JOB_ID,
        status="success",
        order_by="-id",
    )


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs_list_status(dbtc_client):
    data = dbtc_client.cloud.list_runs(
        account_id=ACCOUNT_ID,
        job_definition_id=JOB_ID,
        status=["queued", "starting", "running"],
    )
    status_filters = data["extra"]["filters"]["status__in"]
    assert set(status_filters) == {1, 2, 3}


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs_str_status(dbtc_client):
    data = dbtc_client.cloud.list_runs(
        account_id=ACCOUNT_ID,
        job_definition_id=JOB_ID,
        status="success",
    )
    status_filters = data["extra"]["filters"]["status__in"]
    assert set(status_filters) == {10}


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs_bad_status(dbtc_client):
    with pytest.raises(AttributeError):
        _test_cloud_method(
            dbtc_client, "list_runs", job_definition_id=JOB_ID, status="successs"
        )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_run(dbtc_client):
    _test_cloud_method(dbtc_client, "get_run", run_id=pytest.run_id)


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_most_recent_run(dbtc_client):
    _test_cloud_method(dbtc_client, "get_most_recent_run")


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_most_recent_run_bad(dbtc_client):
    data = dbtc_client.cloud.get_most_recent_run(account_id=1)
    assert "data" in data
    assert data["data"] is None


@pytest.mark.dependency(dpeends=["test_list_runs"])
def test_get_run_timing_details(dbtc_client):
    _test_cloud_method(
        dbtc_client,
        "get_run_timing_details",
        project_id=PROJECT_ID,
        run_id=pytest.run_id,
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_list_run_artifacts(dbtc_client):
    _test_cloud_method(
        dbtc_client,
        "list_run_artifacts",
        run_id=pytest.run_id,
    )


@pytest.mark.dependency(depends=["test_list_run_artifacts"])
def test_get_run_artifact(dbtc_client):
    data = dbtc_client.cloud.get_run_artifact(
        account_id=ACCOUNT_ID, run_id=pytest.run_id, path="run_results.json"
    )
    assert "results" in data.keys()


@pytest.mark.dependency(depends=["test_list_run_artifacts"])
def test_get_most_recent_run_artifacts(dbtc_client):
    data = dbtc_client.cloud.get_most_recent_run_artifact(
        account_id=ACCOUNT_ID, path="manifest.json"
    )
    assert "nodes" in data.keys()


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_most_recent_run_artifacts_bad(dbtc_client):
    data = dbtc_client.cloud.get_most_recent_run_artifact(
        account_id=1, path="manifest.json"
    )
    assert "data" in data
    assert data["data"] is None


@pytest.mark.dependency(depends=["test_list_run_artifacts"])
def test_get_run_artifact_sql(dbtc_client):
    data = dbtc_client.cloud.get_run_artifact(
        account_id=ACCOUNT_ID,
        run_id=pytest.run_id,
        path="compiled/tpch/models/marts/intermediate/order_items.sql",
    )
    assert isinstance(data, str)


@pytest.mark.dependency()
def test_create_webhook(dbtc_client):
    _test_and_set(
        dbtc_client,
        "create_webhook",
        "webhook_id",
        account_id=ACCOUNT_ID,
        payload={
            "name": "Test webhook",
            "active": True,
            "client_url": "https://not-a-real-url.com",
            "event_types": ["job.run.started"],
        },
    )


@pytest.mark.dependency(depends=["test_create_webhook"])
def test_list_webhooks(dbtc_client):
    _test_cloud_method(dbtc_client, "list_webhooks")


@pytest.mark.dependency(depends=["test_create_webhook"])
def test_get_webhook(dbtc_client):
    _test_cloud_method(dbtc_client, "get_webhook", webhook_id=pytest.webhook_id)


@pytest.mark.dependency(depends=["test_create_webhook"])
def test_update_webhook(dbtc_client):
    _test_cloud_method(
        dbtc_client,
        "update_webhook",
        webhook_id=pytest.webhook_id,
        payload={
            "description": "Updating webhook",
            "name": "Test webhook (changed)",
            "active": True,
            "client_url": "https://not-a-real-url.com",
            "event_types": ["job.run.started"],
        },
    )


@pytest.mark.dependency(depends=["test_create_webhook"])
def test_test_webhook(dbtc_client):
    _test_cloud_method(dbtc_client, "test_webhook", webhook_id=pytest.webhook_id)


@pytest.mark.dependency(depends=["test_create_webhook"])
def test_delete_webhook(dbtc_client):
    _test_cloud_method(dbtc_client, "delete_webhook", webhook_id=pytest.webhook_id)
