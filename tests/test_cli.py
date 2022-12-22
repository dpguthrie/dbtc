# stdlib
import json

# third party
import pytest
from typer.testing import CliRunner

# first party
from dbtc.cli import app

runner = CliRunner()


def _test_cloud_cli(commands, variable: str = None):
    result = runner.invoke(app, commands)
    data = json.loads(result.stdout)
    assert result.exit_code == 0
    try:
        assert data['status']['code'] == 200
    except KeyError:
        pass
    if variable is not None:
        setattr(pytest, variable, data['data'][0]['id'])


@pytest.mark.dependency()
def test_list_accounts():
    _test_cloud_cli(['list-accounts'], 'account_id')


@pytest.mark.dependency(depends=['test_list_accounts'])
def test_get_account():
    _test_cloud_cli(['get-account', '--account-id', pytest.account_id])


@pytest.mark.dependency(depends=['test_get_account'])
def test_list_projects():
    _test_cloud_cli(['list-projects', '--account-id', pytest.account_id], 'project_id')


@pytest.mark.dependency(depends=['test_list_projects'])
def test_get_project():
    _test_cloud_cli(
        [
            'get-project',
            '--account-id',
            pytest.account_id,
            '--project-id',
            pytest.project_id,
        ]
    )


@pytest.mark.dependency(depends=['test_list_projects'])
def test_list_jobs():
    _test_cloud_cli(
        [
            'list-jobs',
            '--account-id',
            pytest.account_id,
            '--project-id',
            pytest.project_id,
        ],
        'job_id',
    )


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_get_job():
    _test_cloud_cli(
        [
            'get-job',
            '--account-id',
            pytest.account_id,
            '--job-id',
            pytest.job_id,
        ],
    )


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_list_runs():
    _test_cloud_cli(
        ['list-runs', '--account-id', pytest.account_id, '--job-id', pytest.job_id],
        'run_id',
    )


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_list_runs_list_status():
    _test_cloud_cli(
        [
            'list-runs',
            '--account-id',
            pytest.account_id,
            '--job-id',
            pytest.job_id,
            '--status',
            '["success", "error"]',
        ]
    )


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_list_runs_str_status():
    _test_cloud_cli(
        [
            'list-runs',
            '--account-id',
            pytest.account_id,
            '--job-id',
            pytest.job_id,
            '--status',
            'queued',
        ]
    )


@pytest.mark.dependency(depends=['test_list_runs'])
def test_get_run():
    _test_cloud_cli(
        [
            'get-run',
            '--account-id',
            pytest.account_id,
            '--run-id',
            pytest.run_id,
        ],
    )


@pytest.mark.dependency(depends=['test_list_runs'])
def test_get_most_recent_run():
    _test_cloud_cli(
        [
            'get-most-recent-run',
            '--account-id',
            pytest.account_id,
        ],
    )


@pytest.mark.dependency(depends=['test_list_runs'])
def test_list_run_artifacts():
    _test_cloud_cli(
        [
            'list-run-artifacts',
            '--account-id',
            pytest.account_id,
            '--run-id',
            pytest.run_id,
        ],
    )


@pytest.mark.dependency(depends=['test_list_runs'])
def test_get_run_artifact():
    _test_cloud_cli(
        [
            'get-run-artifact',
            '--account-id',
            pytest.account_id,
            '--run-id',
            pytest.run_id,
            '--path',
            'run_results.json',
        ],
    )


@pytest.mark.dependency(depends=['test_list_runs'])
def test_get_most_recent_run_artifact():
    _test_cloud_cli(
        [
            'get-most-recent-run-artifact',
            '--account-id',
            pytest.account_id,
            '--path',
            'manifest.json',
        ],
    )
