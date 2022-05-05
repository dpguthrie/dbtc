# third party
import pytest


def _test_cloud_method(dbtc_client, method: str, **kwargs):
    "Assert that response status code is 200"
    response = getattr(dbtc_client.cloud, method)(
        account_id=pytest.account_id, **kwargs
    )
    assert response['status']['code'] == 200


def _test_and_set(dbtc_client, method: str, variable: str, **kwargs):
    response = getattr(dbtc_client.cloud, method)(**kwargs)
    setattr(pytest, variable, response['data'][0]['id'])
    assert True


def test_no_access(dbtc_client):
    try:
        response = dbtc_client.cloud.list_projects(account_id=0)
        response['data'][0]['id']
        assert False
    except TypeError:
        assert response['status']['code'] == 404


@pytest.mark.dependency()
def test_list_accounts(dbtc_client):
    _test_and_set(dbtc_client, 'list_accounts', 'account_id')


@pytest.mark.dependency(depends=['test_list_accounts'])
def test_get_account(dbtc_client):
    _test_cloud_method(dbtc_client, 'get_account')


@pytest.mark.dependency(depends=['test_list_accounts'])
def test_get_account_licenses(dbtc_client):
    _test_cloud_method(dbtc_client, 'get_account_licenses')


@pytest.mark.dependency(depends=['test_list_accounts'])
def test_list_invited_users(dbtc_client):
    _test_cloud_method(dbtc_client, 'list_invited_users')


@pytest.mark.dependency(depends=['test_list_accounts'])
def test_list_projects(dbtc_client):
    _test_and_set(
        dbtc_client, 'list_projects', 'project_id', account_id=pytest.account_id
    )


@pytest.mark.dependency(depends=['test_list_projects'])
def test_list_users(dbtc_client):
    _test_and_set(dbtc_client, 'list_users', 'user_id', account_id=pytest.account_id)


@pytest.mark.dependency(depends=['test_list_projects'])
def test_get_project(dbtc_client):
    _test_cloud_method(dbtc_client, 'get_project', project_id=pytest.project_id)


@pytest.mark.dependency(depends=['test_list_users'])
def test_get_user(dbtc_client):
    _test_cloud_method(dbtc_client, 'get_user', user_id=pytest.user_id)


@pytest.mark.dependency(depends=['test_list_projects'])
def test_list_jobs(dbtc_client):
    _test_and_set(
        dbtc_client,
        'list_jobs',
        'job_id',
        account_id=pytest.account_id,
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


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_list_runs_v4(dbtc_client):
    _test_cloud_method(dbtc_client, 'list_runs_v4', account_id=pytest.account_id)


@pytest.mark.dependency(depends=['test_list_runs'])
def test_get_run(dbtc_client):
    _test_cloud_method(dbtc_client, 'get_run', run_id=pytest.run_id)


@pytest.mark.dependency(depends=['test_list_runs'])
def test_get_run_v4(dbtc_client):
    _test_cloud_method(
        dbtc_client, 'get_run_v4', account_id=pytest.account_id, run_id=pytest.run_id
    )


@pytest.mark.dependency(depends=['test_list_runs'])
def test_list_run_artifacts(dbtc_client):
    _test_cloud_method(
        dbtc_client,
        'list_run_artifacts',
        run_id=pytest.run_id,
    )


@pytest.mark.dependency(depends=['test_list_run_artifacts'])
def test_get_run_artifact(dbtc_client):
    data = dbtc_client.cloud.get_run_artifact(
        account_id=pytest.account_id, run_id=pytest.run_id, path='run_results.json'
    )
    assert 'results' in data.keys()
