# stdlib
import json
from typing import List, Optional

# third party
import typer

# first party
from dbtc import dbtCloudClient as dbtc

app = typer.Typer()


valid_inclusions = ['trigger', 'environment', 'run_steps', 'job', 'repository']


def complete_inclusion(ctx, param, incomplete):
    for inclusion in valid_inclusions:
        if inclusion.startswith(incomplete):
            yield inclusion


API_KEY_OPTION = typer.Option(
    None, '--api-key', envvar='DBT_CLOUD_API_KEY', help="User's dbt Cloud API Key"
)
TOKEN_OPTION = typer.Option(
    None,
    '--token',
    envvar='DBT_CLOUD_SERVICE_TOKEN',
    help='Service token for dbt Cloud Account.',
)
HOST_OPTION = typer.Option(
    None,
    '--host',
    envvar='DBT_CLOUD_HOST',
    help='Only used for single tenant instances.',
)
ACCOUNT_ID = typer.Option(
    ...,
    '--account-id',
    '-a',
    envvar='DBT_CLOUD_ACCOUNT_ID',
    help='Numeric ID of account to retrieve.',
)
RUN_ID = typer.Option(..., '--run-id', '-r', help='Numeric ID of run to retrieve.')
JOB_ID = typer.Option(..., '--job-id', '-j', help='Numeric ID of job to retrieve.')
PAYLOAD = typer.Option(
    ...,
    '--payload',
    '-d',
    help='String representation of dictionary needed to create or update resource.',
)
ORDER_BY = typer.Option(
    None,
    '--order-by',
    '-o',
    help='Field to order the result by.  Use `-` to indicate reverse order.',
)
INCLUDE_RELATED = typer.Option(
    None,
    '--include-related',
    '-i',
    help='List of related fields to pull with run',
    shell_complete=complete_inclusion,
)
OFFSET = typer.Option(
    None,
    help='Offset to apply when listing runs.  Use with `limit` to paginate results.',
)
LIMIT = typer.Option(
    None,
    help='Limit to apply when listing runs.  Use with `offset` to paginate results.',
)


def _dbt_cloud_request(ctx: typer.Context, method: str, **kwargs):
    data = getattr(dbtc(**ctx.obj).cloud, method)(**kwargs)
    typer.echo(json.dumps(data))
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
    """Get an account by its ID."""
    _dbt_cloud_request(ctx, 'get_account', account_id=account_id)


@app.command()
def list_projects(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """List projects for a specified account

    Args:
        account_id (int): Numerc ID of the account to retrieve
    """
    _dbt_cloud_request(ctx, 'list_projects', account_id=account_id)


@app.command()
def get_project(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = typer.Option(
        ..., '--project-id', '-p', help='Numeric ID of the project to retrieve.'
    ),
):
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
    project_id: int = typer.Option(
        None, '--project-id', '-p', help='Numeric ID of the project to retrieve.'
    ),
    order_by: str = ORDER_BY,
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
def create_job(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """Create a job in a project."""
    _dbt_cloud_request(
        ctx, 'create_job', account_id=account_id, payload=json.loads(payload)
    )


@app.command()
def get_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    order_by: str = ORDER_BY,
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
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
):
    """Update the definition of an existing job."""
    _dbt_cloud_request(
        ctx,
        'update_job',
        account_id=account_id,
        job_id=job_id,
        payload=json.loads(payload),
    )


@app.command()
def trigger_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
):
    """Trigger job to run."""
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
    include_related: List[str] = INCLUDE_RELATED,
    job_id: int = typer.Option(
        None, '--job-id', '-j', help='Numeric ID of job to retrieve'
    ),
    order_by: str = ORDER_BY,
    offset: int = OFFSET,
    limit: int = LIMIT,
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
        job_definition_id=job_id,
        order_by=order_by,
        offset=offset,
        limit=limit,
    )


@app.command()
def get_run(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    include_related: List[str] = INCLUDE_RELATED,
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
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    step: int = typer.Option(None, '--step', '-s'),
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
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    path: str = typer.Option(..., '--path', '-t'),
    step: int = typer.Option(None, '--step', '-s'),
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
