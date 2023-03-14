# stdlib
import json

# third party
import pytest
from typer.testing import CliRunner

# first party
from dbtc.cli import app

ACCOUNT_ID = 43786
PROJECT_ID = 146088
JOB_ID = 229335

runner = CliRunner()


def _test_cloud_cli(commands, variable: str = None):
    result = runner.invoke(app, commands)
    response = json.loads(result.stdout)
    assert result.exit_code == 0
    try:
        assert 200 <= response['status']['code'] <= 299
    except KeyError:
        pass
    if variable is not None:
        data = response['data']
        if isinstance(data, list):
            setattr(pytest, variable, data[0]['id'])
        else:
            setattr(pytest, variable, data['id'])


@pytest.mark.dependency()
def test_list_accounts():
    _test_cloud_cli(['list-accounts'], 'account_id')


@pytest.mark.dependency(depends=['test_list_accounts'])
def test_get_account():
    _test_cloud_cli(['get-account', '--account-id', ACCOUNT_ID])


@pytest.mark.dependency(depends=['test_get_account'])
def test_list_projects():
    _test_cloud_cli(['list-projects', '--account-id', ACCOUNT_ID], 'project_id')


@pytest.mark.dependency(depends=['test_list_projects'])
def test_get_project():
    _test_cloud_cli(
        [
            'get-project',
            '--account-id',
            ACCOUNT_ID,
            '--project-id',
            PROJECT_ID,
        ]
    )


@pytest.mark.dependency(depends=['test_list_projects'])
def test_list_jobs():
    _test_cloud_cli(
        [
            'list-jobs',
            '--account-id',
            ACCOUNT_ID,
            '--project-id',
            PROJECT_ID,
        ],
    )


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_get_job():
    _test_cloud_cli(
        [
            'get-job',
            '--account-id',
            ACCOUNT_ID,
            '--job-id',
            JOB_ID,
        ],
    )


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_list_runs():
    _test_cloud_cli(
        ['list-runs', '--account-id', ACCOUNT_ID, '--job-id', JOB_ID],
        'run_id',
    )


@pytest.mark.dependency(depends=['test_list_jobs'])
def test_list_runs_list_status():
    _test_cloud_cli(
        [
            'list-runs',
            '--account-id',
            ACCOUNT_ID,
            '--job-id',
            JOB_ID,
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
            ACCOUNT_ID,
            '--job-id',
            JOB_ID,
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
            ACCOUNT_ID,
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
            ACCOUNT_ID,
        ],
    )


@pytest.mark.dependency(depends=['test_list_runs'])
def test_list_run_artifacts():
    _test_cloud_cli(
        [
            'list-run-artifacts',
            '--account-id',
            ACCOUNT_ID,
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
            ACCOUNT_ID,
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
            ACCOUNT_ID,
            '--path',
            'manifest.json',
        ],
    )


@pytest.mark.dependency()
def test_create_webhook():
    _test_cloud_cli(
        [
            'create-webhook',
            '--account-id',
            ACCOUNT_ID,
            '--payload',
            '{"name": "Test webhook", "active": true, '
            '"client_url": "https://not-a-real-url.com", '
            '"event_types": ["job.run.started"]}',
        ],
        'webhook_id',
    )


@pytest.mark.dependency(depends=['test_create_webhook'])
def test_list_webhook():
    _test_cloud_cli(['list-webhooks', '--account-id', ACCOUNT_ID])


@pytest.mark.dependency(depends=['test_create_webhook'])
def test_get_webhook():
    _test_cloud_cli(
        [
            'get-webhook',
            '--account-id',
            ACCOUNT_ID,
            '--webhook-id',
            pytest.webhook_id,
        ],
    )


@pytest.mark.dependency()
def test_update_webhook():
    _test_cloud_cli(
        [
            'update-webhook',
            '--account-id',
            ACCOUNT_ID,
            '--webhook-id',
            pytest.webhook_id,
            '--payload',
            '{"name": "Updating webhook", "active": true, '
            '"client_url": "https://not-a-real-url.com", '
            '"event_types": ["job.run.started"]}',
        ],
    )


@pytest.mark.dependency(depends=['test_create_webhook'])
def test_test_webhook():
    _test_cloud_cli(
        [
            'test-webhook',
            '--account-id',
            ACCOUNT_ID,
            '--webhook-id',
            pytest.webhook_id,
        ],
    )


@pytest.mark.dependency(depends=['test_create_webhook'])
def test_delete_webhook():
    _test_cloud_cli(
        [
            'delete-webhook',
            '--account-id',
            ACCOUNT_ID,
            '--webhook-id',
            pytest.webhook_id,
        ],
    )
