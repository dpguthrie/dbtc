# stdlib
import json
from typing import Optional

# third party
import typer

# first party
from dbtc import __version__
from dbtc import dbtCloudClient as dbtc
from dbtc.console import console

app = typer.Typer()


valid_inclusions = ['trigger', 'environment', 'run_steps', 'job', 'repository']


def version_callback(called: bool):
    if called:
        typer.echo(f'dbtc version: {__version__}')
        raise typer.Exit()


def complete_inclusion(ctx, param, incomplete):
    for inclusion in valid_inclusions:
        if inclusion.startswith(incomplete):
            yield inclusion


ACCOUNT_ID = typer.Option(
    ...,
    '--account-id',
    '-a',
    envvar='DBT_CLOUD_ACCOUNT_ID',
    help='Numeric ID of account to retrieve.',
)
API_KEY = typer.Option(
    None, '--api-key', envvar='DBT_CLOUD_API_KEY', help="User's dbt Cloud API Key"
)
CONNECTION_ID = typer.Option(
    ..., '--connection-id', '-c', help='Numeric ID of the connection.'
)
DO_NOT_TRACK = typer.Option(False, '--do-not-track', help='Turn off tracking')
ENVIRONMENT_ID = typer.Option(
    ..., '--environment-id', '-e', help='Numeric ID of the connection.'
)
GROUP_ID = typer.Option(
    ..., '--group-id', '-g', help='Numeric ID of the group to retrieve.'
)
HOST = typer.Option(
    None,
    '--host',
    envvar='DBT_CLOUD_HOST',
    help='Only used for single tenant instances.',
)
INCLUDE_RELATED = typer.Option(
    None,
    '--include-related',
    '-i',
    help='List of related fields to pull with run',
    shell_complete=complete_inclusion,
)
JOB_ID = typer.Option(..., '--job-id', '-j', help='Numeric ID of job to retrieve.')
LIMIT = typer.Option(
    None,
    help='Limit to apply when listing runs.  Use with `offset` to paginate results.',
)
OFFSET = typer.Option(
    None,
    help='Offset to apply when listing runs.  Use with `limit` to paginate results.',
)
ORDER_BY = typer.Option(
    None,
    '--order-by',
    '-o',
    help='Field to order the result by.  Use `-` to indicate reverse order.',
)
PAYLOAD = typer.Option(
    ...,
    '--payload',
    '-d',
    help='String representation of dictionary needed to create or update resource.',
)
PROJECT_ID = typer.Option(
    ...,
    '--project-id',
    '-p',
    envvar='DBT_CLOUD_PROJECT_ID',
    help='Numeric ID of the project to retrieve.',
)
REPOSITORY_ID = typer.Option(
    ..., '--repository-id', '-y', help='Numeric ID of the repository.'
)
RUN_ID = typer.Option(..., '--run-id', '-r', help='Numeric ID of run to retrieve.')
RUN_ID_OPTIONAL = typer.Option(
    None, '--run-id', '-r', help='Numeric ID of run to retrieve.'
)
SERVICE_TOKEN_ID = typer.Option(
    ..., '--service-token-id', '-t', help='Numeric ID of the service token.'
)
STATE = typer.Option(None, '--state', help='1 = active, 2 = deleted')
TOKEN = typer.Option(
    None,
    '--token',
    envvar='DBT_CLOUD_SERVICE_TOKEN',
    help='Service token for dbt Cloud Account.',
)
UNIQUE_ID = typer.Option(
    ..., '--unique-id', help='The unique ID of this particular object.'
)
USER_ID = typer.Option(..., '--user-id', '-u', help='Numeric ID of the user.')

VERSION = typer.Option(
    None,
    '--version',
    '-v',
    help='Show installed version of dbtc.',
    callback=version_callback,
    is_eager=True,
)
WEBHOOK_ID = typer.Option(..., '--webhook-id', '-w', help='String ID of the webhook')


def _dbt_api_request(ctx: typer.Context, property: str, method: str, *args, **kwargs):
    instance = dbtc(**ctx.obj)
    api = getattr(instance, property)
    data = getattr(api, method)(*args, **kwargs)
    console.print_json(json.dumps(data))


def _dbt_cloud_request(ctx: typer.Context, method: str, *args, **kwargs):
    if kwargs.get('include_related', None) is not None:
        try:
            include_related = kwargs['include_related']
            kwargs['include_related'] = json.loads(include_related)
        except ValueError as e:
            raise ValueError(f'"{include_related}" is not a valid JSON string') from e
    _dbt_api_request(ctx, 'cloud', method, *args, **kwargs)


def _dbt_metadata_request(ctx: typer.Context, method: str, *args, **kwargs):
    _dbt_api_request(ctx, 'metadata', method, *args, **kwargs)


@app.callback()
def common(
    ctx: typer.Context,
    api_key: Optional[str] = API_KEY,
    service_token: Optional[str] = TOKEN,
    host: Optional[str] = HOST,
    do_not_track: Optional[bool] = DO_NOT_TRACK,
    version: Optional[bool] = VERSION,
):
    ctx.params.pop('version')
    ctx.obj = ctx.params
    pass


@app.command()
def assign_group_permissions(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    group_id: int = GROUP_ID,
    payload: str = PAYLOAD,
):
    """Assign group permissions."""
    _dbt_cloud_request(
        ctx,
        'assign_group_permissions',
        account_id,
        group_id,
        json.loads(payload),
    )


@app.command()
def assign_service_token_permissions(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    service_token_id: int = SERVICE_TOKEN_ID,
    payload: str = PAYLOAD,
):
    """Assign permissions to a service token."""
    _dbt_cloud_request(
        ctx,
        'assign_service_token_permissions',
        account_id,
        service_token_id,
        json.loads(payload),
    )


@app.command()
def assign_user_to_group(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Assign a user to a group."""
    _dbt_cloud_request(
        ctx,
        'assign_user_to_group',
        account_id,
        project_id,
        json.loads(payload),
    )


@app.command()
def cancel_run(ctx: typer.Context, account_id: int = ACCOUNT_ID, run_id: int = RUN_ID):
    """Cancel a run."""
    _dbt_cloud_request(ctx, 'cancel_run', account_id, run_id)


@app.command()
def create_adapter(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create an adapter."""
    _dbt_cloud_request(
        ctx, 'create_adapter', account_id, project_id, json.loads(payload)
    )


@app.command()
def create_connection(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create a connection."""
    _dbt_cloud_request(
        ctx, 'create_connection', account_id, project_id, json.loads(payload)
    )


@app.command()
def create_credentials(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create credentials."""
    _dbt_cloud_request(
        ctx, 'create_credentials', account_id, project_id, json.loads(payload)
    )


@app.command()
def create_environment(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create an environment."""
    _dbt_cloud_request(
        ctx, 'create_environment', account_id, project_id, json.loads(payload)
    )


@app.command()
def create_environment_variables(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create environment variables."""
    _dbt_cloud_request(
        ctx, 'create_environment_variables', account_id, project_id, json.loads(payload)
    )


@app.command()
def create_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create a job in a project."""
    _dbt_cloud_request(ctx, 'create_job', account_id, project_id, json.loads(payload))


@app.command()
def create_project(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """Create a project."""
    _dbt_cloud_request(ctx, 'create_project', account_id, json.loads(payload))


@app.command()
def create_repository(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create a repository in a project."""
    _dbt_cloud_request(
        ctx, 'create_repository', account_id, project_id, json.loads(payload)
    )


@app.command()
def create_service_token(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """Create a service token."""
    _dbt_cloud_request(ctx, 'create_service_token', account_id, json.loads(payload))


@app.command()
def create_user_group(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """Create a user group."""
    _dbt_cloud_request(ctx, 'create_user_group', account_id, json.loads(payload))


@app.command()
def create_webhook(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """Create a webhook."""
    _dbt_cloud_request(ctx, 'create_webhook', account_id, json.loads(payload))


@app.command()
def deactivate_user_license(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    permission_id: int = typer.Option(..., '--permission-id'),
    payload: str = PAYLOAD,
):
    """Deactive a user license."""
    _dbt_cloud_request(
        ctx, 'deactivate_user_license', account_id, permission_id, json.loads(payload)
    )


@app.command()
def delete_connection(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    connection_id: int = CONNECTION_ID,
):
    """Delete a connection"""
    _dbt_cloud_request(ctx, 'delete_connection', account_id, project_id, connection_id)


@app.command()
def delete_environment(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    environment_id: int = ENVIRONMENT_ID,
):
    """Delete an environment"""
    _dbt_cloud_request(
        ctx, 'delete_environment', account_id, project_id, environment_id
    )


@app.command()
def delete_environment_variables(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Delete environment variables"""
    _dbt_cloud_request(
        ctx,
        'delete_environment_variables',
        account_id,
        project_id,
        json.loads(payload),
    )


@app.command()
def delete_project(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """Delete a project."""
    _dbt_cloud_request(ctx, 'delete_project', account_id, project_id)


@app.command()
def delete_repository(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    repository_id: int = REPOSITORY_ID,
):
    """Delete a repository."""
    _dbt_cloud_request(ctx, 'delete_repository', account_id, project_id, repository_id)


@app.command()
def delete_user_group(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    group_id: int = GROUP_ID,
):
    """Delete a user group."""
    _dbt_cloud_request(ctx, 'delete_user_group', account_id, group_id)


@app.command()
def delete_webhook(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
):
    """Delete a webhook."""
    _dbt_cloud_request(ctx, 'delete_webhook', account_id, webhook_id)


@app.command()
def get_account(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """Get an account by its ID."""
    _dbt_cloud_request(ctx, 'get_account', account_id)


@app.command()
def get_account_by_name(
    ctx: typer.Context,
    account_name: str = typer.Option(..., '--account-name', help='Name of account'),
):
    """Get an account by its ID."""
    _dbt_cloud_request(ctx, 'get_account_by_name', account_name)


@app.command()
def get_account_licenses(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """Get an account by its ID."""
    _dbt_cloud_request(ctx, 'get_account_licenses', account_id)


@app.command()
def get_exposure(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    name: str = typer.Option(..., '--name', help='Name of the exposure to retrieve'),
    run_id: int = RUN_ID_OPTIONAL,
):
    """Query information about a particular exposure."""
    _dbt_metadata_request(ctx, 'get_exposure', job_id, name, run_id=run_id)


@app.command()
def get_exposures(
    ctx: typer.Context, job_id: int = JOB_ID, run_id: int = RUN_ID_OPTIONAL
):
    """Query information about all exposures in a given job."""
    _dbt_metadata_request(ctx, 'get_exposures', job_id, run_id=run_id)


@app.command()
def get_macro(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    unique_id: str = UNIQUE_ID,
    run_id: int = RUN_ID_OPTIONAL,
):
    """Query information about a particular macro."""
    _dbt_metadata_request(ctx, 'get_macro', job_id, unique_id, run_id=run_id)


@app.command()
def get_macros(ctx: typer.Context, job_id: int = JOB_ID, run_id: int = RUN_ID_OPTIONAL):
    """Query information about all macros in a given job."""
    _dbt_metadata_request(ctx, 'get_macros', job_id, run_id=run_id)


@app.command()
def get_metric(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    unique_id: str = UNIQUE_ID,
    run_id: int = RUN_ID_OPTIONAL,
):
    """Query information about a particular metric."""
    _dbt_metadata_request(ctx, 'get_metric', job_id, unique_id, run_id=run_id)


@app.command()
def get_metrics(
    ctx: typer.Context, job_id: int = JOB_ID, run_id: int = RUN_ID_OPTIONAL
):
    """Query information about all metrics in a given job."""
    _dbt_metadata_request(ctx, 'get_metrics', job_id, run_id=run_id)


@app.command()
def get_model(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    unique_id: str = UNIQUE_ID,
    run_id: int = RUN_ID_OPTIONAL,
):
    """Query information about a particular model."""
    _dbt_metadata_request(ctx, 'get_model', job_id, unique_id, run_id=run_id)


@app.command()
def get_model_by_environment(
    ctx: typer.Context,
    environment_id: int = ENVIRONMENT_ID,
    unique_id: str = UNIQUE_ID,
    last_run_count: int = typer.Option(
        10,
        '--last-run-count',
        help='Number of run results where this model was built to return (max of 10)',
    ),
    with_catalog: bool = typer.Option(
        False,
        '--with-catalog',
        help='If true, return only runs that have catalog information for this model',
    ),
):
    """Query information about a particular model based on environment_id."""
    _dbt_metadata_request(
        ctx,
        'get_model_by_environment',
        environment_id,
        unique_id,
        last_run_count=last_run_count,
        with_catalog=with_catalog,
    )


@app.command()
def get_models(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    run_id: int = RUN_ID_OPTIONAL,
    database: str = typer.Option(
        None, '--database', help='The database where this table/view lives'
    ),
    schema: str = typer.Option(
        None, '--schema', help='The schema where this table/view lives'
    ),
    identifier: str = typer.Option(
        None, '--identifier', help='The identifier of this table/view'
    ),
):
    """Query information about all models in a given job."""
    _dbt_metadata_request(
        ctx,
        'get_models',
        job_id,
        run_id=run_id,
        database=database,
        schema=schema,
        identifier=identifier,
    )


@app.command()
def get_most_recent_run(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    include_related: str = INCLUDE_RELATED,
    job_id: int = typer.Option(
        None, '--job-id', '-j', help='Numeric ID of job to retrieve'
    ),
    environment_id: int = typer.Option(
        None, '--environment-id', '-e', help='Numeric ID of environment to retrieve'
    ),
    project_id: str = typer.Option(
        None, '--project-id', '-p', help='The project ID or IDs'
    ),
    deferring_run_id: int = typer.Option(
        None, '--deferring-run-id', help='The deferring run ID'
    ),
    status: str = typer.Option(
        None, '--status', help='Status to apply when listing runs'
    ),
):
    if status is not None:
        try:
            status = json.loads(status)
        except ValueError:
            pass

    _dbt_cloud_request(
        ctx,
        'get_most_recent_run',
        account_id,
        include_related=include_related,
        job_definition_id=job_id,
        environment_id=environment_id,
        project_id=json.loads(project_id) if project_id else project_id,
        deferring_run_id=deferring_run_id,
        status=status,
    )


@app.command()
def get_most_recent_run_artifact(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    path: str = typer.Option(
        ..., '--path', '-f', help='Name of artifact to retrieve (e.g. manifest.json)'
    ),
    job_id: int = typer.Option(
        None, '--job-id', '-j', help='Numeric ID of job to retrieve'
    ),
    environment_id: int = typer.Option(
        None, '--environment-id', '-e', help='Numeric ID of environment to retrieve'
    ),
    project_id: str = typer.Option(
        None, '--project-id', '-p', help='The project ID or IDs'
    ),
    deferring_run_id: int = typer.Option(
        None, '--deferring-run-id', help='The deferring run ID'
    ),
    step: int = typer.Option(
        None, '--step', '-s', help='Index of the step in the run to retrieve'
    ),
):
    _dbt_cloud_request(
        ctx,
        'get_most_recent_run_artifact',
        account_id,
        path,
        job_definition_id=job_id,
        environment_id=environment_id,
        project_id=json.loads(project_id) if project_id else project_id,
        deferring_run_id=deferring_run_id,
        step=step,
    )


@app.command()
def get_seed(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    unique_id: str = UNIQUE_ID,
    run_id: int = RUN_ID_OPTIONAL,
):
    """Query information about a particular seed."""
    _dbt_metadata_request(ctx, 'get_seed', job_id, unique_id, run_id=run_id)


@app.command()
def get_seeds(ctx: typer.Context, job_id: int = JOB_ID, run_id: int = RUN_ID_OPTIONAL):
    """Query information about all seeds in a given job."""
    _dbt_metadata_request(ctx, 'get_seeds', job_id, run_id=run_id)


@app.command()
def get_snapshot(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    unique_id: str = UNIQUE_ID,
    run_id: int = RUN_ID_OPTIONAL,
):
    """Query information about a particular snapshot."""
    _dbt_metadata_request(ctx, 'get_snapshot', job_id, unique_id, run_id=run_id)


@app.command()
def get_snapshots(
    ctx: typer.Context, job_id: int = JOB_ID, run_id: int = RUN_ID_OPTIONAL
):
    """Query information about all snapshots in a given job."""
    _dbt_metadata_request(ctx, 'get_snapshots', job_id, run_id=run_id)


@app.command()
def get_source(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    unique_id: str = UNIQUE_ID,
    run_id: int = RUN_ID_OPTIONAL,
):
    """Query information about a particular source."""
    _dbt_metadata_request(ctx, 'get_source', job_id, unique_id, run_id=run_id)


@app.command()
def get_sources(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    run_id: int = RUN_ID_OPTIONAL,
    database: str = typer.Option(
        None, '--database', help='The database where this table/view lives'
    ),
    schema: str = typer.Option(
        None, '--schema', help='The schema where this table/view lives'
    ),
    identifier: str = typer.Option(
        None, '--identifier', help='The identifier of this table/view'
    ),
):
    """Query information about all sources in a given job."""
    _dbt_metadata_request(
        ctx,
        'get_sources',
        job_id,
        run_id=run_id,
        database=database,
        schema=schema,
        identifier=identifier,
    )


@app.command()
def get_test(
    ctx: typer.Context,
    job_id: int = JOB_ID,
    unique_id: str = UNIQUE_ID,
    run_id: int = RUN_ID_OPTIONAL,
):
    """Query information about a particular test."""
    _dbt_metadata_request(ctx, 'get_test', job_id, unique_id, run_id=run_id)


@app.command()
def get_tests(ctx: typer.Context, job_id: int = JOB_ID, run_id: int = RUN_ID_OPTIONAL):
    """Query information about all tests in a given job."""
    _dbt_metadata_request(ctx, 'get_tests', job_id, run_id=run_id)


@app.command()
def get_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    order_by: str = ORDER_BY,
):
    """Return job details for a job on an account."""
    _dbt_cloud_request(
        ctx,
        'get_job',
        account_id,
        job_id,
        order_by=order_by,
    )


@app.command()
def get_project(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """Get a project by its ID"""
    _dbt_cloud_request(ctx, 'get_project', account_id=account_id, project_id=project_id)


@app.command()
def get_project_by_name(
    ctx: typer.Context,
    project_name: str = typer.Option(..., '--project-name', help='Name of project'),
    account_id: str = typer.Option(
        None, '--account-id', '-a', help='Numeric ID of account'
    ),
    account_name: str = typer.Option(None, '--account-name', help='Name of account'),
):
    """Get a project by its name."""
    _dbt_cloud_request(
        ctx,
        'get_project_by_name',
        project_name,
        account_id=account_id,
        account_name=account_name,
    )


@app.command()
def get_run(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    include_related: str = INCLUDE_RELATED,
):
    """Get run by ID for a specific account."""
    _dbt_cloud_request(
        ctx,
        'get_run',
        account_id,
        run_id,
        include_related=include_related,
    )


@app.command()
def get_run_artifact(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    path: str = typer.Option(
        ..., '--path', '-f', help='Name of artifact to retrieve (e.g. manifest.json)'
    ),
    step: int = typer.Option(
        None, '--step', '-s', help='Index of the step in the run to retrieve'
    ),
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


@app.command()
def get_run_timing_details(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    run_id: int = RUN_ID,
):
    """Get run timing details for specific run."""
    _dbt_cloud_request(
        ctx,
        'get_run_timing_details',
        account_id,
        project_id,
        run_id,
    )


@app.command()
def get_user(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    user_id: int = USER_ID,
):
    """Get a user."""
    _dbt_cloud_request(
        ctx,
        'get_user',
        account_id,
        user_id,
    )


@app.command()
def get_webhook(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
):
    """Get a webhook by its ID"""
    _dbt_cloud_request(ctx, 'get_webhook', account_id=account_id, webhook_id=webhook_id)


@app.command()
def list_accounts(ctx: typer.Context):
    """List of accounts that your API Token is authorized to access."""
    _dbt_cloud_request(ctx, 'list_accounts')


@app.command()
def list_audit_logs(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    logged_at_start: str = typer.Option(
        None, '--logged-at-start', help='Date to begin retrieving audit logs'
    ),
    logged_at_end: str = typer.Option(
        None, '--logged-at-end', help='Date to stop retrieving audit logs'
    ),
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """Retrieve audit logs for an account."""
    _dbt_cloud_request(
        ctx,
        'list_audit_logs',
        account_id,
        logged_at_start=logged_at_start,
        logged_at_end=logged_at_end,
        offset=offset,
        limit=limit,
    )


@app.command()
def list_connections(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """List connections for a specific account and project."""
    _dbt_cloud_request(ctx, 'list_connections', account_id, project_id)


@app.command()
def list_credentials(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """List credentials for a specific account and project."""
    _dbt_cloud_request(ctx, 'list_credentials', account_id, project_id)


@app.command()
def list_environments(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: str = typer.Option(
        None, '--project-id', '-p', help='The project ID or IDs'
    ),
    dbt_version: str = typer.Option(
        None,
        '--dbt-version',
        help='The dbt version(s) used in the environment',
    ),
    name: str = typer.Option(
        None,
        '--name',
        help='The name of the environment',
    ),
    type: str = typer.Option(
        None,
        '--type',
        help='The type of environment (deployment or development)',
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
    order_by: str = ORDER_BY,
):
    """List environments in an account"""
    try:
        dbt_version = json.loads(dbt_version)
    except (ValueError, TypeError):
        pass

    _dbt_cloud_request(
        ctx,
        'list_environments',
        account_id,
        project_id=json.loads(project_id) if project_id else project_id,
        dbt_version=dbt_version,
        name=name,
        type=type,
        state=state,
        offset=offset,
        limit=limit,
        order_by=order_by,
    )


@app.command()
def list_feature_flags(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """List feature flags for a specific account."""
    _dbt_cloud_request(ctx, 'list_feature_flags', account_id)


@app.command()
def list_groups(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """List groups for a specific account."""
    _dbt_cloud_request(ctx, 'list_groups', account_id)


@app.command()
def list_invited_users(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """List invited users for a specific account."""
    _dbt_cloud_request(ctx, 'list_invited_users', account_id)


@app.command()
def list_jobs(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    environment_id: int = typer.Option(
        None,
        '--environment-id',
        '-e',
        help='Numeric ID of the environment to retrieve',
    ),
    project_id: str = typer.Option(
        None, '--project-id', '-p', help='The project ID or IDs'
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
    order_by: str = ORDER_BY,
):
    """List jobs in an account or specific project"""
    _dbt_cloud_request(
        ctx,
        'list_jobs',
        account_id,
        environment_id=environment_id,
        project_id=json.loads(project_id) if project_id else project_id,
        state=state,
        offset=offset,
        limit=limit,
        order_by=order_by,
    )


@app.command()
def list_projects(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: str = typer.Option(
        None, '--project-id', '-p', help='The project ID or IDs'
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """List projects for a specified account"""
    _dbt_cloud_request(
        ctx,
        'list_projects',
        account_id,
        project_id=json.loads(project_id) if project_id else project_id,
        state=state,
        offset=offset,
        limit=limit,
    )


@app.command()
def list_repositories(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """List repositories for a specific account and project."""
    _dbt_cloud_request(ctx, 'list_repositories', account_id, project_id)


@app.command()
def list_run_artifacts(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    step: int = typer.Option(None, '--step', '-s'),
):
    """List run artifacts

    Use this endpoint to fetch a list of artifact fiels generated for a completed run.

    !!! note
        By default, this endpoint returns artifacts from the last step in the run.
        To list artifacts from other steps in the run, use the `step` query parameter.
    """
    _dbt_cloud_request(ctx, 'list_run_artifacts', account_id, run_id, step=step)


@app.command()
def list_runs(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    include_related: str = INCLUDE_RELATED,
    job_id: int = typer.Option(
        None, '--job-id', '-j', help='Numeric ID of job to retrieve'
    ),
    environment_id: int = typer.Option(
        None, '--environment-id', '-e', help='Numeric ID of environment to retrieve'
    ),
    project_id: str = typer.Option(
        None, '--project-id', '-p', help='The project ID or IDs'
    ),
    deferring_run_id: int = typer.Option(
        None, '--deferring-run-id', help='The deferring run ID'
    ),
    status: str = typer.Option(
        None, '--status', help='Status to apply when listing runs'
    ),
    order_by: str = ORDER_BY,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    if status is not None:
        try:
            status = json.loads(status)
        except ValueError:
            pass
    """List runs for a specific account."""
    _dbt_cloud_request(
        ctx,
        'list_runs',
        account_id,
        include_related=include_related,
        job_definition_id=job_id,
        environment_id=environment_id,
        project_id=json.loads(project_id) if project_id else project_id,
        deferring_run_id=deferring_run_id,
        order_by=order_by,
        offset=offset,
        limit=limit,
        status=status,
    )


@app.command()
def list_service_token_permissions(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    service_token_id: int = SERVICE_TOKEN_ID,
):
    """List service token permissions for a specific account."""
    _dbt_cloud_request(
        ctx, 'list_service_token_permissions', account_id, service_token_id
    )


@app.command()
def list_users(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    order_by: str = ORDER_BY,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """List users for a specific account."""
    _dbt_cloud_request(
        ctx,
        'list_users',
        account_id,
        order_by=order_by,
        offset=offset,
        limit=limit,
    )


@app.command()
def list_webhooks(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """List webhooks for a specific account."""
    _dbt_cloud_request(
        ctx,
        'list_webhooks',
        account_id,
        offset=offset,
        limit=limit,
    )


@app.command()
def test_connection(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Test a warehouse connection."""
    _dbt_cloud_request(
        ctx,
        'test_connection',
        account_id,
        project_id,
        json.loads(payload),
    )


@app.command()
def test_webhook(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
):
    """Test a webhook."""
    _dbt_cloud_request(
        ctx,
        'test_webhook',
        account_id,
        webhook_id,
    )


@app.command()
def trigger_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
    should_poll: bool = typer.Option(
        True,
        help='Poll until job completion (status is one of success, failure, or '
        'cancelled)',
    ),
    poll_interval: int = typer.Option(
        10, '--poll-interval', help='Number of seconds to wait in between polling.'
    ),
):
    """Trigger job to run."""
    _dbt_cloud_request(
        ctx,
        'trigger_job',
        account_id,
        job_id,
        json.loads(payload),
        should_poll=should_poll,
        poll_interval=poll_interval,
    )


@app.command()
def trigger_autoscaling_ci_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
    should_poll: bool = typer.Option(
        False,
        help='Poll until job completion (status is one of success, failure, or '
        'cancelled)',
    ),
    poll_interval: int = typer.Option(
        10, '--poll-interval', help='Number of seconds to wait in between polling.'
    ),
    delete_cloned_job: bool = typer.Option(
        True, help='Indicate whether cloned job should be deleted after triggering'
    ),
    max_run_slots: int = typer.Option(
        None, help='Number of run slots that should be available to this process'
    ),
):
    """Trigger an autoscaling CI job to run."""
    _dbt_cloud_request(
        ctx,
        'trigger_autoscaling_ci_job',
        account_id,
        job_id,
        json.loads(payload),
        should_poll=should_poll,
        poll_interval=poll_interval,
        delete_cloned_job=delete_cloned_job,
        max_run_slots=max_run_slots,
    )


@app.command()
def trigger_job_from_failure(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
    should_poll: bool = typer.Option(
        True,
        help='Poll until job completion (status is one of success, failure, or '
        'cancelled)',
    ),
    poll_interval: int = typer.Option(
        10, '--poll-interval', help='Number of seconds to wait in between polling.'
    ),
    trigger_on_failure_only: bool = typer.Option(
        False,
        help=(
            'Only relevant when setting restart_from_failure to True.  This has the '
            'effect of only triggering the job when the prior invocation was not '
            'successful. Otherwise, the function will exit prior to triggering the '
            'job.'
        ),
    ),
):
    """Trigger job from point of failure."""
    _dbt_cloud_request(
        ctx,
        'trigger_job_from_failure',
        account_id,
        job_id,
        json.loads(payload),
        should_poll=should_poll,
        poll_interval=poll_interval,
        trigger_on_failure_only=trigger_on_failure_only,
    )


@app.command()
def update_connection(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    connection_id: int = CONNECTION_ID,
    payload: str = PAYLOAD,
):
    """Update a connection."""
    _dbt_cloud_request(
        ctx,
        'update_connection',
        account_id,
        project_id,
        connection_id,
        json.loads(payload),
    )


@app.command()
def update_credentials(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    credentials_id: int = typer.Option(
        ..., '--credentials-id', help='Numeric ID of the credentials.'
    ),
    payload: str = PAYLOAD,
):
    """Update credentials."""
    _dbt_cloud_request(
        ctx,
        'update_credentials',
        account_id,
        project_id,
        credentials_id,
        json.loads(payload),
    )


@app.command()
def update_environment(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    environment_id: int = ENVIRONMENT_ID,
    payload: str = PAYLOAD,
):
    """Update an environment."""
    _dbt_cloud_request(
        ctx,
        'update_environment',
        account_id,
        project_id,
        environment_id,
        json.loads(payload),
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
        account_id,
        job_id,
        json.loads(payload),
    )


@app.command()
def update_project(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Update a project."""
    _dbt_cloud_request(
        ctx,
        'update_project',
        account_id,
        project_id,
        json.loads(payload),
    )


@app.command()
def update_repository(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    repository_id: int = REPOSITORY_ID,
    payload: str = PAYLOAD,
):
    """Update a repository."""
    _dbt_cloud_request(
        ctx,
        'update_repository',
        account_id,
        project_id,
        repository_id,
        json.loads(payload),
    )


@app.command()
def update_webhook(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
    payload: str = PAYLOAD,
):
    """Update a webhook."""
    _dbt_cloud_request(
        ctx,
        'update_webhook',
        account_id,
        webhook_id,
        json.loads(payload),
    )


def main():
    app()
