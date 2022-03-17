# third party
import pytest


def _test_cloud_method(dbtc_client, method: str, **kwargs):
    "Assert that response status code is 200"
    response = getattr(dbtc_client.cloud, method)(
        account_id=pytest.account_id, **kwargs
    )
    if response['status']['code'] == 200:
        assert True
    else:
        assert False


def _test_and_set(dbtc_client, method: str, variable: str, **kwargs):
    response = getattr(dbtc_client.cloud, method)(**kwargs)
    try:
        setattr(pytest, variable, response['data'][0]['id'])
        assert True
    except (TypeError, IndexError):
        assert False


@pytest.mark.dependency()
def test_list_accounts(dbtc_client):
    _test_and_set(dbtc_client, 'list_accounts', 'account_id')


@pytest.mark.dependency(depends=['test_list_accounts'])
def test_get_account(dbtc_client):
    _test_cloud_method(dbtc_client, 'get_account')


@pytest.mark.dependency(depends=['test_list_accounts'])
def test_list_projects(dbtc_client):
    _test_and_set(
        dbtc_client, 'list_projects', 'project_id', account_id=pytest.account_id
    )
    _test_cloud_method(dbtc_client, 'list_projects')


@pytest.mark.dependency(depends=['test_list_projects'])
def test_get_project(dbtc_client):
    _test_cloud_method(dbtc_client, 'get_project', project_id=pytest.project_id)


@pytest.mark.dependency(depends=['test_list_projects'])
def test_list_jobs(dbtc_client):
    _test_and_set(
        dbtc_client,
        'list_jobs',
        'job_id',
        account_id=pytest.account_id,
        project_id=pytest.project_id,
    )


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_get_job(dbtc_client):
    _test_cloud_method(dbtc_client, 'get_job', job_id=pytest.job_id)


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_list_runs(dbtc_client):
    _test_and_set(
        dbtc_client,
        'list_runs',
        'run_id',
        account_id=pytest.account_id,
        job_definition_id=pytest.job_id,
    )


@pytest.mark.dependency(depends=['test_list_runs'])
def test_get_run(dbtc_client):
    _test_cloud_method(dbtc_client, 'get_run', run_id=pytest.run_id)


@pytest.mark.dependency(depends=['test_list_runs'])
def test_list_run_artifacts(dbtc_client):
    _test_and_set(
        dbtc_client,
        'list_run_artifacts',
        'path',
        account_id=pytest.account_id,
        run_id=pytest.run_id,
    )


@pytest.mark.dependency(depends=['test_list_run_artifacts'])
def test_get_run_artifact(dbtc_client):
    _test_cloud_method(
        dbtc_client,
        'get_run_artifact',
        account_id=pytest.account_id,
        run_id=pytest.run_id,
        path=pytest.path,
    )
