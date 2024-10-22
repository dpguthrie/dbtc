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
        assert 200 <= response["status"]["code"] <= 299
    except KeyError:
        pass
    if variable is not None:
        data = response["data"]
        if isinstance(data, list):
            setattr(pytest, variable, data[0]["id"])
        else:
            setattr(pytest, variable, data["id"])


@pytest.mark.dependency()
def test_list_accounts():
    _test_cloud_cli(["list-accounts"], "account_id")


@pytest.mark.dependency(depends=["test_list_accounts"])
def test_get_account_old():
    _test_cloud_cli(["get-account", "--account-id", ACCOUNT_ID])


@pytest.mark.dependency(depends=["test_list_accounts"])
def test_get_account():
    _test_cloud_cli(["accounts", "get", "--account-id", ACCOUNT_ID])


@pytest.mark.dependency(depends=["test_get_account"])
def test_list_projects_old():
    _test_cloud_cli(["list-projects", "--account-id", ACCOUNT_ID], "project_id")


@pytest.mark.dependency(depends=["test_get_account"])
def test_list_projects():
    _test_cloud_cli(["projects", "list", "--account-id", ACCOUNT_ID], "project_id")


@pytest.mark.dependency(depends=["test_list_projects"])
def test_get_project_old():
    _test_cloud_cli(
        [
            "get-project",
            "--account-id",
            ACCOUNT_ID,
            "--project-id",
            PROJECT_ID,
        ]
    )


def test_get_project():
    _test_cloud_cli(
        [
            "projects",
            "get",
            "--account-id",
            ACCOUNT_ID,
            "--project-id",
            PROJECT_ID,
        ]
    )


@pytest.mark.dependency(depends=["test_list_projects"])
def test_list_environments_old():
    _test_cloud_cli(
        [
            "list-environments",
            "--account-id",
            ACCOUNT_ID,
            "--project-id",
            PROJECT_ID,
        ],
    )


@pytest.mark.dependency(depends=["test_list_projects"])
def test_list_environments():
    _test_cloud_cli(
        [
            "environments",
            "list",
            "--account-id",
            ACCOUNT_ID,
            "--project-id",
            PROJECT_ID,
        ],
    )


@pytest.mark.dependency(depends=["test_list_projects"])
def test_list_jobs_old():
    _test_cloud_cli(
        [
            "list-jobs",
            "--account-id",
            ACCOUNT_ID,
            "--project-id",
            PROJECT_ID,
        ],
    )


@pytest.mark.dependency(depends=["test_list_projects"])
def test_list_jobs():
    _test_cloud_cli(
        [
            "jobs",
            "list",
            "--account-id",
            ACCOUNT_ID,
            "--project-id",
            PROJECT_ID,
        ],
    )


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_get_job_old():
    _test_cloud_cli(
        [
            "get-job",
            "--account-id",
            ACCOUNT_ID,
            "--job-id",
            JOB_ID,
        ],
    )


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_get_job():
    _test_cloud_cli(
        [
            "jobs",
            "get",
            "--account-id",
            ACCOUNT_ID,
            "--job-id",
            JOB_ID,
        ],
    )


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs_old():
    _test_cloud_cli(
        ["list-runs", "--account-id", ACCOUNT_ID, "--job-id", JOB_ID],
    )


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs():
    _test_cloud_cli(
        [
            "runs",
            "list",
            "--account-id",
            ACCOUNT_ID,
            "--job-id",
            JOB_ID,
            "--status",
            "success",
            "--order-by",
            "-id",
        ],
        "run_id",
    )


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs_list_status_old():
    _test_cloud_cli(
        [
            "list-runs",
            "--account-id",
            ACCOUNT_ID,
            "--job-id",
            JOB_ID,
            "--status",
            '["success", "error"]',
        ]
    )


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs_list_status():
    _test_cloud_cli(
        [
            "runs",
            "list",
            "--account-id",
            ACCOUNT_ID,
            "--job-id",
            JOB_ID,
            "--status",
            '["success", "error"]',
        ]
    )


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs_str_status_old():
    _test_cloud_cli(
        [
            "list-runs",
            "--account-id",
            ACCOUNT_ID,
            "--job-id",
            JOB_ID,
            "--status",
            "queued",
        ]
    )


@pytest.mark.dependency(depends=["test_list_jobs"])
def test_list_runs_str_status():
    _test_cloud_cli(
        [
            "runs",
            "list",
            "--account-id",
            ACCOUNT_ID,
            "--job-id",
            JOB_ID,
            "--status",
            "queued",
        ]
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_run_old():
    _test_cloud_cli(
        [
            "get-run",
            "--account-id",
            ACCOUNT_ID,
            "--run-id",
            pytest.run_id,
        ],
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_run():
    _test_cloud_cli(
        [
            "runs",
            "get",
            "--account-id",
            ACCOUNT_ID,
            "--run-id",
            pytest.run_id,
        ],
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_most_recent_run_old():
    _test_cloud_cli(
        [
            "get-most-recent-run",
            "--account-id",
            ACCOUNT_ID,
        ],
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_most_recent_run():
    _test_cloud_cli(
        [
            "runs",
            "get-most-recent",
            "--account-id",
            ACCOUNT_ID,
        ],
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_list_run_artifacts_old():
    _test_cloud_cli(
        [
            "list-run-artifacts",
            "--account-id",
            ACCOUNT_ID,
            "--run-id",
            pytest.run_id,
        ],
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_list_run_artifacts():
    _test_cloud_cli(
        [
            "runs",
            "list-artifacts",
            "--account-id",
            ACCOUNT_ID,
            "--run-id",
            pytest.run_id,
        ],
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_run_artifact_old():
    _test_cloud_cli(
        [
            "get-run-artifact",
            "--account-id",
            ACCOUNT_ID,
            "--run-id",
            pytest.run_id,
            "--path",
            "manifest.json",
        ],
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_run_artifact():
    _test_cloud_cli(
        [
            "runs",
            "get-artifact",
            "--account-id",
            ACCOUNT_ID,
            "--run-id",
            pytest.run_id,
            "--path",
            "manifest.json",
        ],
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_most_recent_run_artifact_old():
    _test_cloud_cli(
        [
            "get-most-recent-run-artifact",
            "--account-id",
            ACCOUNT_ID,
            "--path",
            "manifest.json",
        ],
    )


@pytest.mark.dependency(depends=["test_list_runs"])
def test_get_most_recent_run_artifact():
    _test_cloud_cli(
        [
            "runs",
            "get-most-recent-artifact",
            "--account-id",
            ACCOUNT_ID,
            "--path",
            "manifest.json",
        ],
    )


@pytest.mark.dependency()
def test_create_webhook():
    _test_cloud_cli(
        [
            "webhooks",
            "create",
            "--account-id",
            ACCOUNT_ID,
            "--payload",
            '{"name": "Test webhook", "active": true, '
            '"client_url": "https://not-a-real-url.com", '
            '"event_types": ["job.run.started"]}',
        ],
        "webhook_id",
    )


@pytest.mark.dependency(depends=["test_create_webhook"])
def test_list_webhook():
    _test_cloud_cli(["webhooks", "list", "--account-id", ACCOUNT_ID])


@pytest.mark.dependency(depends=["test_create_webhook"])
def test_get_webhook():
    _test_cloud_cli(
        [
            "webhooks",
            "get",
            "--account-id",
            ACCOUNT_ID,
            "--webhook-id",
            pytest.webhook_id,
        ],
    )


@pytest.mark.dependency()
def test_update_webhook():
    _test_cloud_cli(
        [
            "webhooks",
            "update",
            "--account-id",
            ACCOUNT_ID,
            "--webhook-id",
            pytest.webhook_id,
            "--payload",
            '{"name": "Updating webhook", "active": true, '
            '"client_url": "https://not-a-real-url.com", '
            '"event_types": ["job.run.started"]}',
        ],
    )


@pytest.mark.dependency(depends=["test_create_webhook"])
def test_test_webhook():
    _test_cloud_cli(
        [
            "webhooks",
            "test",
            "--account-id",
            ACCOUNT_ID,
            "--webhook-id",
            pytest.webhook_id,
        ],
    )


@pytest.mark.dependency(depends=["test_create_webhook"])
def test_delete_webhook():
    _test_cloud_cli(
        [
            "webhooks",
            "delete",
            "--account-id",
            ACCOUNT_ID,
            "--webhook-id",
            pytest.webhook_id,
        ],
    )
