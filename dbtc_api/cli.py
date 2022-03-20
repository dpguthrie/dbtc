# stdlib
import json
from typing import List, Optional

# third party
import typer

# first party
from dbtc_api import dbtCloudClient as dbtc

app = typer.Typer()

API_KEY_OPTION = typer.Option(
    None, envvar='DBT_CLOUD_API_KEY', help="User's dbt Cloud API Key"
)
TOKEN_OPTION = typer.Option(
    None, envvar='DBT_CLOUD_SERVICE_TOKEN', help='Service token for dbt Cloud Account'
)
HOST_OPTION = typer.Option(
    None, envvar='DBT_CLOUD_HOST', help='Only used for single tenant instances'
)
ACCOUNT_ID = typer.Option(..., '--account-id', envvar='DBT_CLOUD_ACCOUNT_ID')


def _dbt_cloud_request(ctx: typer.Context, method: str, **kwargs):
    data = getattr(dbtc(**ctx.obj).cloud, method)(**kwargs)
    typer.echo(data)
    return data


@app.callback()
def common(
    ctx: typer.Context,
    api_key: Optional[str] = API_KEY_OPTION,
    service_token: Optional[str] = TOKEN_OPTION,
    host: Optional[str] = HOST_OPTION,
):
    ctx.obj = ctx.params
    pass


@app.command()
def list_accounts(ctx: typer.Context):
    """List of accounts that your API Token is authorized to access."""
    _dbt_cloud_request(ctx, 'list_accounts')


@app.command()
def get_account(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """Get an account by its ID

    Args:
        account_id (int): Numeric ID of the account to retrieve
    """
    _dbt_cloud_request(ctx, 'get_account', account_id=account_id)


@app.command()
def list_projects(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """List projects for a specified account

    Args:
        account_id (int): Numerc ID of the account to retrieve
    """
    _dbt_cloud_request(ctx, 'list_projects', account_id=account_id)


@app.command()
def get_project(ctx: typer.Context, project_id: int, account_id: int = ACCOUNT_ID):
    """Get a project by its ID

    Args:
        account_id (int): Numerc ID of the account to retrieve
        project_id (int): Numeric ID of the project to retrieve
    """
    _dbt_cloud_request(ctx, 'get_project', account_id=account_id, project_id=project_id)


@app.command()
def list_jobs(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    order_by: str = None,
    project_id: int = None,
):
    """List jobs in an account or specific project

    Args:
        account_id (int): Numerc ID of the account to retrieve
        project_id (:obj:`int`, optional): Numeric ID of the project containing jobs
        order_by (:obj:`str`, optional): Field to order the result by.
            Use `-` to indicate reverse order.
    """
    _dbt_cloud_request(
        ctx,
        'list_jobs',
        account_id=account_id,
        order_by=order_by,
        project_id=project_id,
    )


@app.command()
def create_job(ctx: typer.Context, payload: str, account_id: int = ACCOUNT_ID):
    """Create a job in a project.

    Args:
        account_id (int): Numerc ID of the account to retrieve
        payload: (dict):
            account_id: int, required
            project_id: int, required
            environment_id: int, required
            name: str, required
                Name for the job
            execute_steps, List[str], required
                Array of commands to execute
            dbt_version, str, optional
                Overrides dbt_version specified on the attached Environment if provided
            triggers: Dict, optional, one of:
                github_webhook: bool
                schedule: bool
                custom_branch_only: bool
            settings: Dict, optional
                threads: int
                    Maximum number of models to runi n parallel in a single dbt run
                target_name: str
                    Informational field that can be consumed in dbt project code with
                    {{ target.name }}
            state: int, optional
                1 = active
                2 = deleted
            generate_docs:  bool, optional
                When true, run a `dbt docs generate` step at the end of runs
                triggered from this job
            schedule: Dict, optional
                cron: str
                    Cron-syntax schedule for the job
                date: str, one of:
                    every_day, days_of_week, custom_cron
                tyoe: str, one of:
                    every_hour, at_exact_hours
    """
    _dbt_cloud_request(
        ctx, 'create_job', account_id=account_id, payload=json.loads(payload)
    )


@app.command()
def get_job(
    ctx: typer.Context,
    job_id: int,
    account_id: int = ACCOUNT_ID,
    order_by: str = None,
):
    """Return job details for a job on an account.

    Args:
        account_id (int): Numerc ID of the account containing the job
        job_id (int): Numeric ID of the job to retrieve
        order_by (:obj:`str`, optional): Field to order the result by.
            Use `-` to indicate reverse order.
    """
    _dbt_cloud_request(
        ctx,
        'get_job',
        account_id=account_id,
        job_id=job_id,
        order_by=order_by,
    )


@app.command()
def update_job(
    ctx: typer.Context, job_id: int, payload: str, account_id: int = ACCOUNT_ID
):
    """Update the definition of an existing job.

    Args:
        account_id (int): Numerc ID of the account that the Job belongs to
        job_id (:obj:`int`, optional): Numeric ID of the job to update
    """
    _dbt_cloud_request(
        ctx,
        'update_job',
        account_id=account_id,
        job_id=job_id,
        payload=json.loads(payload),
    )


@app.command()
def trigger_job(
    ctx: typer.Context, job_id: int, payload: str, account_id: int = ACCOUNT_ID
):
    """Trigger job to run

    Use this endpoint to kick off a run for a job.  When this endpoint returns a
    successful response, a new run will be enqueued for the account.  Users can poll
    the Get Run endpoint to poll the run until it completes.  After the run has
    completed, users can use the get run artifact endpoint to download artifacts
    generated by the run.

    Args:
        account_id (int): Numerc ID of the account that the Job belongs to
        job_id (:obj:`int`, optional): Numeric ID of the job to run
    """
    _dbt_cloud_request(
        ctx,
        'update_job',
        account_id=account_id,
        job_id=job_id,
        payload=json.loads(payload),
    )


@app.command()
def list_runs(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    include_related: List[str] = None,
    job_definition_id: int = None,
    order_by: str = None,
    offset: int = None,
    limit: int = None,
):
    """List runs for a specific account.

    Args:
        account_id (int): Numerc ID of the account to retrieve
        include_related (:obj:`str`, optional): List of related fields to pull with
            the run.  Valid values are "trigger", "job", "repository", and
            "environment".

    """
    _dbt_cloud_request(
        ctx,
        'list_runs',
        account_id=account_id,
        include_related=include_related,
        job_definition_id=job_definition_id,
        order_by=order_by,
        offset=offset,
        limit=limit,
    )


@app.command()
def get_run(
    ctx: typer.Context,
    run_id: int,
    account_id: int = ACCOUNT_ID,
    include_related: List[str] = None,
):
    """Get run by ID for a specific account."""
    _dbt_cloud_request(
        ctx,
        'get_run',
        account_id=account_id,
        run_id=run_id,
        include_related=include_related,
    )


@app.command()
def list_run_artifacts(
    ctx: typer.Context, run_id: int, account_id: int = ACCOUNT_ID, step: int = None
):
    """List run artifacts

    Use this endpoint to fetch a list of artifact fiels generated for a completed run.

    Note:  By default, this endpoint returns artifacts from the last step in the run.
    To list artifacts from other steps in the run, use the `step` query parameter.
    """
    _dbt_cloud_request(
        ctx, 'list_run_artifacts', account_id=account_id, run_id=run_id, step=step
    )


@app.command()
def get_run_artifact(
    ctx: typer.Context,
    run_id: int,
    path: str,
    account_id: int = ACCOUNT_ID,
    step: int = None,
):
    """Get a specific run artifact by path

    Use this endpoint to fetch artifacts from a completed run.  Once a run has
    completed, you can use this endpoint to download the `manifest.json`,
    `run_results.json`, or `catalog.json` files from dbt Cloud.  These artifacts
    contain information about the models in your dbt project, timing information
    around their execution, and a status message indicating the result of the model
    build

    Note:  By default, this endpoint returns artifacts from the last step in the run.
    To list artifacts from other steps in the run, use the `step` query parameter.
    """
    _dbt_cloud_request(
        ctx,
        'get_run_artifact',
        account_id=account_id,
        run_id=run_id,
        path=path,
        step=step,
    )


def main():
    app()
