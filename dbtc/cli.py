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


valid_inclusions = ["trigger", "environment", "run_steps", "job", "repository"]


def version_callback(called: bool):
    if called:
        typer.echo(f"dbtc version: {__version__}")
        raise typer.Exit()


def complete_inclusion(ctx, param, incomplete):
    for inclusion in valid_inclusions:
        if inclusion.startswith(incomplete):
            yield inclusion


# region _APPS
accounts_app = typer.Typer()
adapters_app = typer.Typer()
connections_app = typer.Typer()
credentials_app = typer.Typer()
env_vars_app = typer.Typer()
environments_app = typer.Typer()
groups_app = typer.Typer()
jobs_app = typer.Typer()
metadata_app = typer.Typer()
projects_app = typer.Typer()
repos_app = typer.Typer()
runs_app = typer.Typer()
service_tokens_app = typer.Typer()
users_app = typer.Typer()
webhooks_app = typer.Typer()

app.add_typer(accounts_app, name="accounts", help="Manage accounts in dbt Cloud")
app.add_typer(adapters_app, name="adapters", help="Manage adapters in dbt Cloud")
app.add_typer(
    connections_app, name="connections", help="Manage connections in dbt Cloud"
)
app.add_typer(
    credentials_app, name="credentials", help="Manage credentials in dbt Cloud"
)
app.add_typer(
    env_vars_app, name="env-vars", help="Manage environment variables in dbt Cloud"
)
app.add_typer(
    environments_app, name="environments", help="Manage environments in dbt Cloud"
)
app.add_typer(groups_app, name="groups", help="Manage user groups in dbt Cloud")
app.add_typer(jobs_app, name="jobs", help="Manage jobs in dbt Cloud")
app.add_typer(metadata_app, name="metadata", help="Retrieve metadata from dbt Cloud")
app.add_typer(projects_app, name="projects", help="Manage projects in dbt Cloud")
app.add_typer(repos_app, name="repos", help="Manage repositories in dbt Cloud")
app.add_typer(runs_app, name="runs", help="Manage runs in dbt Cloud")
app.add_typer(
    service_tokens_app, name="service-tokens", help="Manage service tokens in dbt Cloud"
)
app.add_typer(users_app, name="users", help="Manage users in dbt Cloud")
app.add_typer(webhooks_app, name="webhooks", help="Manage webhooks in dbt Cloud")

# endregion


# region _VARIABLES

ACCOUNT_ID = typer.Option(
    ...,
    "--account-id",
    "-a",
    envvar="DBT_CLOUD_ACCOUNT_ID",
    help="Numeric ID of account to retrieve.",
)
ADAPTER_ID = typer.Option(
    ...,
    "--adapter-id",
    help="Numeric ID of adapter.",
)
API_KEY = typer.Option(
    None, "--api-key", envvar="DBT_CLOUD_API_KEY", help="User's dbt Cloud API Key"
)
CONNECTION_ID = typer.Option(
    ..., "--connection-id", "-c", help="Numeric ID of the connection."
)
DO_NOT_TRACK = typer.Option(False, "--do-not-track", help="Turn off tracking")
END_DATE = typer.Option(..., "--end-date", help="Date to end retrieving data from")
ENVIRONMENT_ID = typer.Option(
    ..., "--environment-id", "-e", help="Numeric ID of the connection."
)
GROUP_ID = typer.Option(
    ..., "--group-id", "-g", help="Numeric ID of the group to retrieve."
)
HOST = typer.Option(
    None,
    "--host",
    envvar="DBT_CLOUD_HOST",
    help="Used for single tenant instances or multi-tenant regions outside of the US.",
)
INCLUDE_RELATED = typer.Option(
    None,
    "--include-related",
    "-i",
    help="List of related fields to pull with run",
    shell_complete=complete_inclusion,
)
JOB_ID = typer.Option(..., "--job-id", "-j", help="Numeric ID of job to retrieve.")
LIMIT = typer.Option(
    None,
    help="Limit to apply when listing runs.  Use with `offset` to paginate results.",
)
OFFSET = typer.Option(
    None,
    help="Offset to apply when listing runs.  Use with `limit` to paginate results.",
)
OUTPUT = typer.Option(
    None, "--output", "-o", help="Output file to write results to.  Defaults to stdout."
)
ORDER_BY = typer.Option(
    None,
    "--order-by",
    help="Field to order the result by.  Use `-` to indicate reverse order.",
)
PAYLOAD = typer.Option(
    ...,
    "--payload",
    "-d",
    help="String representation of dictionary needed to create or update resource.",
)
PROJECT_ID = typer.Option(
    ...,
    "--project-id",
    "-p",
    envvar="DBT_CLOUD_PROJECT_ID",
    help="Numeric ID of the project to retrieve.",
)
REPOSITORY_ID = typer.Option(
    ..., "--repository-id", "-y", help="Numeric ID of the repository."
)
RUN_ID = typer.Option(..., "--run-id", "-r", help="Numeric ID of run to retrieve.")
RUN_ID_OPTIONAL = typer.Option(
    None, "--run-id", "-r", help="Numeric ID of run to retrieve."
)
SERVICE_TOKEN_ID = typer.Option(
    ..., "--service-token-id", "-t", help="Numeric ID of the service token."
)
START_DATE = typer.Option(
    ..., "--start-date", help="Date to begin retrieving data from"
)
STATE = typer.Option(None, "--state", help="1 = active, 2 = deleted")
TOKEN = typer.Option(
    None,
    "--token",
    envvar="DBT_CLOUD_SERVICE_TOKEN",
    help="Service token for dbt Cloud Account.",
)
UNIQUE_ID = typer.Option(
    ..., "--unique-id", help="The unique ID of this particular object."
)
USER_ID = typer.Option(..., "--user-id", "-u", help="Numeric ID of the user.")

VERSION = typer.Option(
    None,
    "--version",
    "-v",
    help="Show installed version of dbtc.",
    callback=version_callback,
    is_eager=True,
)
WEBHOOK_ID = typer.Option(..., "--webhook-id", "-w", help="String ID of the webhook")

# endregion


# region _COMMON
def _dbt_api_request(ctx: typer.Context, property: str, method: str, *args, **kwargs):
    output = ctx.obj.pop("output", None)
    instance = dbtc(**ctx.obj)
    api = getattr(instance, property)
    data = getattr(api, method)(*args, **kwargs)
    if output:
        with open(output, "w") as f:
            if output.endswith("json"):
                f.write(json.dumps(data))
            else:
                f.write(data)
    else:
        console.print_json(json.dumps(data))


def _dbt_cloud_request(ctx: typer.Context, method: str, *args, **kwargs):
    if kwargs.get("include_related", None) is not None:
        try:
            include_related = kwargs["include_related"]
            kwargs["include_related"] = json.loads(include_related)
        except ValueError as e:
            raise ValueError(f'"{include_related}" is not a valid JSON string') from e
    _dbt_api_request(ctx, "cloud", method, *args, **kwargs)


@app.callback()
def common(
    ctx: typer.Context,
    api_key: Optional[str] = API_KEY,
    service_token: Optional[str] = TOKEN,
    host: Optional[str] = HOST,
    do_not_track: Optional[bool] = DO_NOT_TRACK,
    version: Optional[bool] = VERSION,
    output: Optional[str] = OUTPUT,
):
    ctx.params.pop("version")
    ctx.obj = ctx.params
    pass


# endregion


# region ACCOUNTS
@app.command("get-account", hidden=True)
def get_account_old(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """This will soon be deprecated! Use `dbtc accounts get` instead."""
    return get_account(ctx, account_id)


@accounts_app.command("get")
def get_account(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """Get an account by its ID."""
    _dbt_cloud_request(ctx, "get_account", account_id)


@app.command("get-account-by-name", hidden=True)
def get_account_by_name_old(
    ctx: typer.Context,
    account_name: str = typer.Option(..., "--account-name", help="Name of account"),
):
    """This will soon be deprecated! Use `dbtc accounts get-by-name` instead."""
    return get_account_by_name(ctx, account_name)


@accounts_app.command("get-by-name")
def get_account_by_name(
    ctx: typer.Context,
    account_name: str = typer.Option(..., "--account-name", help="Name of account"),
):
    """Get an account by its name."""
    _dbt_cloud_request(ctx, "get_account_by_name", account_name)


@app.command("get-account-licenses", hidden=True)
def get_account_licenses_old(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """This will soon be deprecated! Use `dbtc accounts get-licenses` instead."""
    return get_account_licenses(ctx, account_id)


@accounts_app.command("get-licenses")
def get_account_licenses(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """Get the licenses for an account."""
    _dbt_cloud_request(ctx, "get_account_licenses", account_id)


@app.command("list-accounts", hidden=True)
def list_accounts_old(ctx: typer.Context):
    """This will soon be deprecated! Use `dbtc accounts list` instead."""
    return list_accounts(ctx)


@accounts_app.command("list")
def list_accounts(ctx: typer.Context):
    """List of accounts that your API Token is authorized to access."""
    _dbt_cloud_request(ctx, "list_accounts")


@app.command("list-audit-logs", hidden=True)
def list_audit_logs_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    logged_at_start: str = typer.Option(
        None, "--logged-at-start", help="Date to begin retrieving audit logs"
    ),
    logged_at_end: str = typer.Option(
        None, "--logged-at-end", help="Date to stop retrieving audit logs"
    ),
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """This will soon be deprecated! Use `dbtc accounts list-audit-logs` instead."""
    return list_audit_logs(
        ctx,
        account_id,
        logged_at_start,
        logged_at_end,
        offset,
        limit,
    )


@accounts_app.command("list-audit-logs")
def list_audit_logs(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    logged_at_start: str = typer.Option(
        None, "--logged-at-start", help="Date to begin retrieving audit logs"
    ),
    logged_at_end: str = typer.Option(
        None, "--logged-at-end", help="Date to stop retrieving audit logs"
    ),
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """Retrieve audit logs for an account."""
    _dbt_cloud_request(
        ctx,
        "list_audit_logs",
        account_id,
        logged_at_start=logged_at_start,
        logged_at_end=logged_at_end,
        offset=offset,
        limit=limit,
    )


@app.command("list-feature-flags", hidden=True)
def list_feature_flags_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
):
    """This will soon be deprecated! Use `dbtc feature-flags list` instead."""
    return list_feature_flags(ctx, account_id)


@accounts_app.command()
def list_feature_flags(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """List feature flags for a specific account."""
    _dbt_cloud_request(ctx, "list_feature_flags", account_id)


# endregion

# region ADAPTERS


@adapters_app.command("create")
def create_adapter(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create an adapter."""
    _dbt_cloud_request(
        ctx, "create_adapter", account_id, project_id, json.loads(payload)
    )


@adapters_app.command("delete")
def delete_adapter(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    adapter_id: int = ADAPTER_ID,
):
    """Delete an adapter."""
    _dbt_cloud_request(ctx, "delete_adapter", account_id, project_id, adapter_id)


@adapters_app.command("get")
def get_adapter(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    adapter_id: int = ADAPTER_ID,
):
    """Get an adapter."""
    _dbt_cloud_request(ctx, "get_adapter", account_id, project_id, adapter_id)


@adapters_app.command("update")
def update_adapter(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    adapter_id: int = ADAPTER_ID,
    payload: str = PAYLOAD,
):
    """Update an adapter."""
    _dbt_cloud_request(
        ctx, "update_adapter", account_id, project_id, adapter_id, payload
    )


# endregion


# region CONNECTIONS
@app.command("create-connection", hidden=True)
def create_connection_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc connections create` instead."""
    return create_connection(ctx, account_id, project_id, payload)


@connections_app.command("create")
def create_connection(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create a connection."""
    _dbt_cloud_request(
        ctx, "create_connection", account_id, project_id, json.loads(payload)
    )


@app.command("delete-connection", hidden=True)
def delete_connection_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    connection_id: int = CONNECTION_ID,
):
    """This will soon be deprecated! Use `dbtc connections delete` instead."""
    return delete_connection(ctx, account_id, project_id, connection_id)


@connections_app.command("delete")
def delete_connection(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    connection_id: int = CONNECTION_ID,
):
    """Delete a connection"""
    _dbt_cloud_request(ctx, "delete_connection", account_id, project_id, connection_id)


@app.command("list-connections", hidden=True)
def list_connections_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """This will soon be deprecated! Use `dbtc connections list` instead."""
    return list_connections(ctx, account_id, project_id)


@connections_app.command("list")
def list_connections(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """List connections for a specific account and project."""
    _dbt_cloud_request(ctx, "list_connections", account_id, project_id)


@app.command("test-connection", hidden=True)
def test_connection_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated!  Use dbtc connections test instead."""
    return test_connection(ctx, account_id, project_id, payload)


@connections_app.command("test")
def test_connection(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    _dbt_cloud_request(
        ctx,
        "test_connection",
        account_id,
        project_id,
        json.loads(payload),
    )


@app.command("update-connection", hidden=True)
def update_connection_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    connection_id: int = CONNECTION_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc connections update` instead."""
    return update_connection(ctx, account_id, project_id, connection_id, payload)


@connections_app.command("update")
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
        "update_connection",
        account_id,
        project_id,
        connection_id,
        json.loads(payload),
    )


# endregion

# region CREDENTIALS


@app.command("create-credentials", hidden=True)
def create_credentials_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc credentials create` instead."""
    return create_credentials(ctx, account_id, project_id, payload)


@credentials_app.command("create")
def create_credentials(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create credentials."""
    _dbt_cloud_request(
        ctx, "create_credentials", account_id, project_id, json.loads(payload)
    )


@app.command("list-credentials", hidden=True)
def list_credentials_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """This will soon be deprecated! Use `dbtc credentials list` instead."""
    return list_credentials(ctx, account_id, project_id)


@credentials_app.command("list")
def list_credentials(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """List credentials for a specific account and project."""
    _dbt_cloud_request(ctx, "list_credentials", account_id, project_id)


@app.command("update-credentials", hidden=True)
def update_credentials_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    credentials_id: int = typer.Option(
        ..., "--credentials-id", help="Numeric ID of the credentials."
    ),
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc credentials update` instead."""
    return update_credentials(ctx, account_id, project_id, credentials_id, payload)


@credentials_app.command("update")
def update_credentials(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    credentials_id: int = typer.Option(
        ..., "--credentials-id", help="Numeric ID of the credentials."
    ),
    payload: str = PAYLOAD,
):
    """Update credentials."""
    _dbt_cloud_request(
        ctx,
        "update_credentials",
        account_id,
        project_id,
        credentials_id,
        json.loads(payload),
    )


# endregion

# region ENV_VARS


@app.command("create-environment-variables", hidden=True)
def create_environment_variables_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc env-vars create` instead."""
    return create_environment_variables(ctx, account_id, project_id, payload)


@env_vars_app.command("create")
def create_environment_variables(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create environment variables."""
    _dbt_cloud_request(
        ctx, "create_environment_variables", account_id, project_id, json.loads(payload)
    )


@app.command("delete-environment-variables", hidden=True)
def delete_environment_variables_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc env-vars delete` instead."""
    return delete_environment_variables(ctx, account_id, project_id, payload)


@env_vars_app.command("delete")
def delete_environment_variables(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Delete environment variables"""
    _dbt_cloud_request(
        ctx,
        "delete_environment_variables",
        account_id,
        project_id,
        json.loads(payload),
    )


@app.command("list-environment-variables", hidden=True)
def list_environment_variables_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    resource_type: str = typer.Option(
        "environment",
        "--resource-type",
        help="The name of the resource to retrieve",
    ),
    environment_id: int = typer.Option(
        None,
        "--environment-id",
        help="Numeric ID of the environment to retrieve",
    ),
    job_id: int = typer.Option(
        None,
        "--job-id",
        help="Numeric ID of the job to retrieve",
    ),
    user_id: int = typer.Option(None, "--user-id", "-u", help="Numeric ID of the user"),
    name: str = typer.Option(
        None,
        "--name",
        help="The name of the environment",
    ),
    type: str = typer.Option(
        None,
        "--type",
        help="The type of environment (deployment or development)",
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """This will soon be deprecated! Use `dbtc env-vars list` instead."""
    return list_environment_variables(
        ctx,
        account_id,
        project_id,
        resource_type,
        environment_id,
        job_id,
        user_id,
        name,
        type,
        state,
        offset,
        limit,
    )


@env_vars_app.command("list")
def list_environment_variables(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    resource_type: str = typer.Option(
        "environment",
        "--resource-type",
        help="The name of the resource to retrieve",
    ),
    environment_id: int = typer.Option(
        None,
        "--environment-id",
        help="Numeric ID of the environment to retrieve",
    ),
    job_id: int = typer.Option(
        None,
        "--job-id",
        help="Numeric ID of the job to retrieve",
    ),
    user_id: int = typer.Option(None, "--user-id", "-u", help="Numeric ID of the user"),
    name: str = typer.Option(
        None,
        "--name",
        help="The name of the environment",
    ),
    type: str = typer.Option(
        None,
        "--type",
        help="The type of environment (deployment or development)",
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    _dbt_cloud_request(
        ctx,
        "list_environment_variables",
        account_id,
        project_id,
        resource_type=resource_type,
        environment_id=environment_id,
        job_id=job_id,
        user_id=user_id,
        name=name,
        type=type,
        state=state,
        offset=offset,
        limit=limit,
    )


@app.command("update-environment-variables", hidden=True)
def update_environment_variables_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc env-vars update` instead."""
    return update_environment_variables(ctx, account_id, project_id, payload)


@env_vars_app.command("update")
def update_environment_variables(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Update environment variables."""
    _dbt_cloud_request(
        ctx,
        "update_environment_variables",
        account_id,
        project_id,
        json.loads(payload),
    )


# endregion

# region ENVIRONMENTS


@app.command("create-environment", hidden=True)
def create_environment_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc environments create` instead."""
    return create_environment(ctx, account_id, project_id, payload)


@environments_app.command("create")
def create_environment(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create an environment."""
    _dbt_cloud_request(
        ctx, "create_environment", account_id, project_id, json.loads(payload)
    )


@app.command("delete-environment", hidden=True)
def delete_environment_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    environment_id: int = ENVIRONMENT_ID,
):
    """This will soon be deprecated! Use `dbtc environments delete` instead."""
    return delete_environment(ctx, account_id, project_id, environment_id)


@environments_app.command("delete")
def delete_environment(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    environment_id: int = ENVIRONMENT_ID,
):
    """Delete an environment"""
    _dbt_cloud_request(
        ctx, "delete_environment", account_id, project_id, environment_id
    )


@app.command("list-environments", hidden=True)
def list_environments_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: str = PROJECT_ID,
    credentials_id: int = typer.Option(
        None, "--credentials-id", help="Numeric ID of the credentials."
    ),
    dbt_version: str = typer.Option(
        None,
        "--dbt-version",
        help="The dbt version(s) used in the environment",
    ),
    deployment_type: str = typer.Option(
        None,
        "--deployment-type",
        help="The deployment type of the environment",
    ),
    name: str = typer.Option(
        None,
        "--name",
        help="The name of the environment",
    ),
    type: str = typer.Option(
        None,
        "--type",
        help="The type of environment (deployment or development)",
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
    order_by: str = ORDER_BY,
):
    """This will soon be deprecated! Use `dbtc environments list` instead."""
    return list_environments(
        ctx,
        account_id,
        project_id,
        credentials_id=credentials_id,
        dbt_version=dbt_version,
        deployment_type=deployment_type,
        name=name,
        type=type,
        state=state,
        offset=offset,
        limit=limit,
        order_by=order_by,
    )


@environments_app.command("list")
def list_environments(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: str = PROJECT_ID,
    dbt_version: str = typer.Option(
        None,
        "--dbt-version",
        help="The dbt version(s) used in the environment",
    ),
    deployment_type: str = typer.Option(
        None,
        "--deployment-type",
        help="The deployment type of the environment",
    ),
    credentials_id: int = typer.Option(
        None, "--credentials-id", help="Numeric ID of the credentials."
    ),
    name: str = typer.Option(
        None,
        "--name",
        help="The name of the environment",
    ),
    type: str = typer.Option(
        None,
        "--type",
        help="The type of environment (deployment or development)",
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

    try:
        deployment_type = json.loads(deployment_type)
    except (ValueError, TypeError):
        pass

    _dbt_cloud_request(
        ctx,
        "list_environments",
        account_id,
        project_id,
        dbt_version=dbt_version,
        deployment_type=deployment_type,
        credentials_id=credentials_id,
        name=name,
        type=type,
        state=state,
        offset=offset,
        limit=limit,
        order_by=order_by,
    )


@app.command("update-environment", hidden=True)
def update_environment_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    environment_id: int = ENVIRONMENT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc environments update` instead."""
    return update_environment(ctx, account_id, project_id, environment_id, payload)


@environments_app.command("update")
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
        "update_environment",
        account_id,
        project_id,
        environment_id,
        json.loads(payload),
    )


# endregion

# region GROUPS


@app.command("assign-group-permissions", hidden=True)
def assign_group_permissions_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    group_id: int = GROUP_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc user-groups assign-permissions`
    instead.
    """
    return assign_group_permissions(ctx, account_id, group_id, payload)


@groups_app.command("assign-permissions")
def assign_group_permissions(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    group_id: int = GROUP_ID,
    payload: str = PAYLOAD,
):
    """Assign group permissions."""
    _dbt_cloud_request(
        ctx,
        "assign_group_permissions",
        account_id,
        group_id,
        json.loads(payload),
    )


@app.command("assign-user-to-group", hidden=True)
def assign_user_to_group_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc users assign-to-group` instead."""
    return assign_user_to_group(ctx, account_id, project_id, payload)


@groups_app.command("assign")
def assign_user_to_group(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Assign a user to a group."""
    _dbt_cloud_request(
        ctx,
        "assign_user_to_group",
        account_id,
        project_id,
        json.loads(payload),
    )


@app.command("create-user-group", hidden=True)
def create_user_group_old(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """This will soon be deprecated! Use `dbtc user-groups create` instead."""
    return create_user_group(ctx, account_id, payload)


@groups_app.command("create")
def create_user_group(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """Create a user group."""
    _dbt_cloud_request(ctx, "create_user_group", account_id, json.loads(payload))


@app.command("delete-user-group", hidden=True)
def delete_user_group_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    group_id: int = GROUP_ID,
):
    """This will soon be deprecated! Use `dbtc user-groups delete` instead."""
    return delete_user_group(ctx, account_id, group_id)


@groups_app.command("delete")
def delete_user_group(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    group_id: int = GROUP_ID,
):
    """Delete a user group."""
    _dbt_cloud_request(ctx, "delete_user_group", account_id, group_id)


@app.command("list-groups", hidden=True)
def list_groups_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
):
    """This will soon be deprecated! Use `dbtc user-groups list` instead."""
    return list_groups(ctx, account_id)


@groups_app.command("list")
def list_groups(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """List groups for a specific account."""
    _dbt_cloud_request(ctx, "list_groups", account_id)


# endregion

# region JOBS


@app.command("create-job", hidden=True)
def create_job_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc jobs create` instead."""
    return create_job(ctx, account_id, project_id, payload)


@jobs_app.command("create")
def create_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create a job in a project."""
    _dbt_cloud_request(ctx, "create_job", account_id, project_id, json.loads(payload))


@app.command("get-job", hidden=True)
def get_job_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    order_by: str = ORDER_BY,
):
    """This will soon be deprecated! Use `dbtc jobs get` instead."""
    return get_job(ctx, account_id, job_id, order_by)


@jobs_app.command("get")
def get_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    order_by: str = ORDER_BY,
):
    """Return job details for a job on an account."""
    _dbt_cloud_request(
        ctx,
        "get_job",
        account_id,
        job_id,
        order_by=order_by,
    )


@app.command("list-jobs", hidden=True)
def list_jobs_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    environment_id: int = typer.Option(
        None,
        "--environment-id",
        "-e",
        help="Numeric ID of the environment to retrieve",
    ),
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
    order_by: str = ORDER_BY,
):
    """This will soon be deprecated! Use `dbtc jobs list` instead."""
    return list_jobs(
        ctx, account_id, environment_id, project_id, state, offset, limit, order_by
    )


@jobs_app.command("list")
def list_jobs(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    environment_id: int = typer.Option(
        None,
        "--environment-id",
        "-e",
        help="Numeric ID of the environment to retrieve",
    ),
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
    order_by: str = ORDER_BY,
):
    """List jobs in an account or specific project"""
    _dbt_cloud_request(
        ctx,
        "list_jobs",
        account_id,
        environment_id=environment_id,
        project_id=json.loads(project_id) if project_id else project_id,
        state=state,
        offset=offset,
        limit=limit,
        order_by=order_by,
    )


@app.command("trigger-job", hidden=True)
def trigger_job_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
    should_poll: bool = typer.Option(
        True,
        help="Poll until job completion (status is one of success, failure, or "
        "cancelled)",
    ),
    poll_interval: int = typer.Option(
        10, "--poll-interval", help="Number of seconds to wait in between polling."
    ),
    retries: int = typer.Option(
        0, "--retries", help="Number of times to retry triggering the job on failure."
    ),
):
    """This will soon be deprecated! Use `dbtc jobs trigger` instead."""
    return trigger_job(
        ctx, account_id, job_id, payload, should_poll, poll_interval, retries
    )


@jobs_app.command("trigger")
def trigger_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
    should_poll: bool = typer.Option(
        True,
        help="Poll until job completion (status is one of success, failure, or "
        "cancelled)",
    ),
    poll_interval: int = typer.Option(
        10, "--poll-interval", help="Number of seconds to wait in between polling."
    ),
    retries: int = typer.Option(
        0, "--retries", help="Number of times to retry triggering the job on failure."
    ),
):
    """Trigger job to run."""
    _dbt_cloud_request(
        ctx,
        "trigger_job",
        account_id,
        job_id,
        json.loads(payload),
        should_poll=should_poll,
        poll_interval=poll_interval,
        retries=retries,
    )


@app.command("trigger-autoscaling-ci-job", hidden=True)
def trigger_autoscaling_ci_job_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
    should_poll: bool = typer.Option(
        False,
        help="Poll until job completion (status is one of success, failure, or "
        "cancelled)",
    ),
    poll_interval: int = typer.Option(
        10, "--poll-interval", help="Number of seconds to wait in between polling."
    ),
    delete_cloned_job: bool = typer.Option(
        True, help="Indicate whether cloned job should be deleted after triggering"
    ),
    max_run_slots: int = typer.Option(
        None, help="Number of run slots that should be available to this process"
    ),
):
    """This will soon be deprecated! Use `dbtc jobs trigger-autoscaling` instead."""
    return trigger_autoscaling_ci_job(
        ctx,
        account_id,
        job_id,
        payload,
        should_poll,
        poll_interval,
        delete_cloned_job,
        max_run_slots,
    )


@jobs_app.command("trigger-autoscaling")
def trigger_autoscaling_ci_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
    should_poll: bool = typer.Option(
        False,
        help="Poll until job completion (status is one of success, failure, or "
        "cancelled)",
    ),
    poll_interval: int = typer.Option(
        10, "--poll-interval", help="Number of seconds to wait in between polling."
    ),
    delete_cloned_job: bool = typer.Option(
        True, help="Indicate whether cloned job should be deleted after triggering"
    ),
    max_run_slots: int = typer.Option(
        None, help="Number of run slots that should be available to this process"
    ),
):
    """Trigger an autoscaling CI job to run."""
    _dbt_cloud_request(
        ctx,
        "trigger_autoscaling_ci_job",
        account_id,
        job_id,
        json.loads(payload),
        should_poll=should_poll,
        poll_interval=poll_interval,
        delete_cloned_job=delete_cloned_job,
        max_run_slots=max_run_slots,
    )


@app.command("trigger-job-from-failure", hidden=True)
def trigger_job_from_failure_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    should_poll: bool = typer.Option(
        True,
        help="Poll until job completion (status is one of success, failure, or "
        "cancelled)",
    ),
    poll_interval: int = typer.Option(
        10, "--poll-interval", help="Number of seconds to wait in between polling."
    ),
):
    """This will soon be deprecated! Use `dbtc jobs trigger-from-failure` instead."""
    return trigger_job_from_failure(ctx, account_id, job_id, should_poll, poll_interval)


@jobs_app.command("trigger-from-failure")
def trigger_job_from_failure(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    should_poll: bool = typer.Option(
        True,
        help="Poll until job completion (status is one of success, failure, or "
        "cancelled)",
    ),
    poll_interval: int = typer.Option(
        10, "--poll-interval", help="Number of seconds to wait in between polling."
    ),
):
    """Trigger job from point of failure."""
    _dbt_cloud_request(
        ctx,
        "trigger_job_from_failure",
        account_id,
        job_id,
        should_poll=should_poll,
        poll_interval=poll_interval,
    )


@app.command("update-job", hidden=True)
def update_job_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc jobs update` instead."""
    return update_job(ctx, account_id, job_id, payload)


@jobs_app.command("update")
def update_job(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    job_id: int = JOB_ID,
    payload: str = PAYLOAD,
):
    """Update the definition of an existing job."""
    _dbt_cloud_request(
        ctx,
        "update_job",
        account_id,
        job_id,
        json.loads(payload),
    )


# endregion

# region PROJECTS


@app.command("create-project", hidden=True)
def create_project_old(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """This will soon be deprecated! Use `dbtc projects create` instead."""
    return create_project(ctx, account_id, payload)


@projects_app.command("create")
def create_project(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """Create a project."""
    _dbt_cloud_request(ctx, "create_project", account_id, json.loads(payload))


@app.command("delete-project", hidden=True)
def delete_project_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """This will soon be deprecated! Use `dbtc projects delete` instead."""
    return delete_project(ctx, account_id, project_id)


@projects_app.command("delete")
def delete_project(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """Delete a project."""
    _dbt_cloud_request(ctx, "delete_project", account_id, project_id)


@app.command("get-project", hidden=True)
def get_project_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """This will soon be deprecated! Use `dbtc projects get` instead."""
    return get_project(ctx, account_id, project_id)


@projects_app.command("get")
def get_project(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """Get a project by its ID"""
    _dbt_cloud_request(ctx, "get_project", account_id=account_id, project_id=project_id)


@app.command("get-project-by-name", hidden=True)
def get_project_by_name_old(
    ctx: typer.Context,
    project_name: str = typer.Option(..., "--project-name", help="Name of project"),
    account_id: str = typer.Option(
        None, "--account-id", "-a", help="Numeric ID of account"
    ),
    account_name: str = typer.Option(None, "--account-name", help="Name of account"),
):
    """This will soon be deprecated! Use `dbtc projects get-by-name` instead."""
    return get_project_by_name(ctx, project_name, account_id, account_name)


@projects_app.command("get-by-name")
def get_project_by_name(
    ctx: typer.Context,
    project_name: str = typer.Option(..., "--project-name", help="Name of project"),
    account_id: str = typer.Option(
        None, "--account-id", "-a", help="Numeric ID of account"
    ),
    account_name: str = typer.Option(None, "--account-name", help="Name of account"),
):
    """Get a project by its name."""
    _dbt_cloud_request(
        ctx,
        "get_project_by_name",
        project_name,
        account_id=account_id,
        account_name=account_name,
    )


@app.command("list-projects", hidden=True)
def list_projects_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """This will soon be deprecated! Use `dbtc projects list` instead."""
    return list_projects(ctx, account_id, project_id, state, offset, limit)


@projects_app.command("list")
def list_projects(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    state: str = STATE,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """List projects for a specified account"""
    _dbt_cloud_request(
        ctx,
        "list_projects",
        account_id,
        project_id=json.loads(project_id) if project_id else project_id,
        state=state,
        offset=offset,
        limit=limit,
    )


@app.command("update-project", hidden=True)
def update_project_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc projects update` instead."""
    return update_project(ctx, account_id, project_id, payload)


@projects_app.command("update")
def update_project(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Update a project."""
    _dbt_cloud_request(
        ctx,
        "update_project",
        account_id,
        project_id,
        json.loads(payload),
    )


# endregion

# region REPOS


@app.command("create-repository", hidden=True)
def create_repository_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc repos create` instead."""
    return create_repository(ctx, account_id, project_id, payload)


@repos_app.command("create")
def create_repository(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    payload: str = PAYLOAD,
):
    """Create a repository in a project."""
    _dbt_cloud_request(
        ctx, "create_repository", account_id, project_id, json.loads(payload)
    )


@app.command("delete-repository", hidden=True)
def delete_repository_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    repository_id: int = REPOSITORY_ID,
):
    """This will soon be deprecated! Use `dbtc repos delete` instead."""
    return delete_repository(ctx, account_id, project_id, repository_id)


@repos_app.command("delete")
def delete_repository(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    repository_id: int = REPOSITORY_ID,
):
    """Delete a repository."""
    _dbt_cloud_request(ctx, "delete_repository", account_id, project_id, repository_id)


@app.command("list-repositories", hidden=True)
def list_repositories_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """This will soon be deprecated! Use `dbtc repos list` instead."""
    return list_repositories(ctx, account_id, project_id)


@repos_app.command("list")
def list_repositories(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
):
    """List repositories for a specific account and project."""
    _dbt_cloud_request(ctx, "list_repositories", account_id, project_id)


@app.command("update-repository", hidden=True)
def update_repository_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    repository_id: int = REPOSITORY_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc repos update` instead."""
    return update_repository(ctx, account_id, project_id, repository_id, payload)


@repos_app.command("update")
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
        "update_repository",
        account_id,
        project_id,
        repository_id,
        json.loads(payload),
    )


# endregion

# region RUNS


@app.command("cancel-run", hidden=True)
def cancel_run_old(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, run_id: int = RUN_ID
):
    """This will soon be deprecated! Use `dbtc runs cancel` instead."""
    return cancel_run(ctx, account_id, run_id)


@runs_app.command("cancel")
def cancel_run(ctx: typer.Context, account_id: int = ACCOUNT_ID, run_id: int = RUN_ID):
    """Cancel a run."""
    _dbt_cloud_request(ctx, "cancel_run", account_id, run_id)


@app.command("get-most-recent-run", hidden=True)
def get_most_recent_run_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    include_related: str = INCLUDE_RELATED,
    job_id: int = typer.Option(
        None, "--job-id", "-j", help="Numeric ID of job to retrieve"
    ),
    environment_id: int = typer.Option(
        None, "--environment-id", "-e", help="Numeric ID of environment to retrieve"
    ),
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    deferring_run_id: int = typer.Option(
        None, "--deferring-run-id", help="The deferring run ID"
    ),
    status: str = typer.Option(
        None, "--status", help="Status to apply when listing runs"
    ),
):
    """This will soon be deprecated! Use `dbtc runs get-most-recent` instead."""
    return get_most_recent_run(
        ctx,
        account_id,
        include_related,
        job_id,
        environment_id,
        project_id,
        deferring_run_id,
        status,
    )


@runs_app.command("get-most-recent")
def get_most_recent_run(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    include_related: str = INCLUDE_RELATED,
    job_id: int = typer.Option(
        None, "--job-id", "-j", help="Numeric ID of job to retrieve"
    ),
    environment_id: int = typer.Option(
        None, "--environment-id", "-e", help="Numeric ID of environment to retrieve"
    ),
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    deferring_run_id: int = typer.Option(
        None, "--deferring-run-id", help="The deferring run ID"
    ),
    status: str = typer.Option(
        None, "--status", help="Status to apply when listing runs"
    ),
):
    """Get the most recent run for an account."""
    if status is not None:
        try:
            status = json.loads(status)
        except ValueError:
            pass

    _dbt_cloud_request(
        ctx,
        "get_most_recent_run",
        account_id,
        include_related=include_related,
        job_definition_id=job_id,
        environment_id=environment_id,
        project_id=json.loads(project_id) if project_id else project_id,
        deferring_run_id=deferring_run_id,
        status=status,
    )


@app.command("get-most-recent-run-artifact", hidden=True)
def get_most_recent_run_artifact_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    path: str = typer.Option(
        ..., "--path", "-f", help="Name of artifact to retrieve (e.g. manifest.json)"
    ),
    job_id: int = typer.Option(
        None, "--job-id", "-j", help="Numeric ID of job to retrieve"
    ),
    environment_id: int = typer.Option(
        None, "--environment-id", "-e", help="Numeric ID of environment to retrieve"
    ),
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    deferring_run_id: int = typer.Option(
        None, "--deferring-run-id", help="The deferring run ID"
    ),
    step: int = typer.Option(
        None, "--step", "-s", help="Index of the step in the run to retrieve"
    ),
):
    """
    This will soon be deprecated! Use `dbtc runs get-most-recent-artifact` instead.
    """
    return get_most_recent_run_artifact(
        ctx,
        account_id,
        path,
        job_id,
        environment_id,
        project_id,
        deferring_run_id,
        step,
    )


@runs_app.command("get-most-recent-artifact")
def get_most_recent_run_artifact(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    path: str = typer.Option(
        ..., "--path", "-f", help="Name of artifact to retrieve (e.g. manifest.json)"
    ),
    job_id: int = typer.Option(
        None, "--job-id", "-j", help="Numeric ID of job to retrieve"
    ),
    environment_id: int = typer.Option(
        None, "--environment-id", "-e", help="Numeric ID of environment to retrieve"
    ),
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    deferring_run_id: int = typer.Option(
        None, "--deferring-run-id", help="The deferring run ID"
    ),
    step: int = typer.Option(
        None, "--step", "-s", help="Index of the step in the run to retrieve"
    ),
):
    """Get an artifact from the most recent run for an account."""
    _dbt_cloud_request(
        ctx,
        "get_most_recent_run_artifact",
        account_id,
        path,
        job_definition_id=job_id,
        environment_id=environment_id,
        project_id=json.loads(project_id) if project_id else project_id,
        deferring_run_id=deferring_run_id,
        step=step,
    )


@app.command("get-run", hidden=True)
def get_run_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    include_related: str = INCLUDE_RELATED,
):
    """This will soon be deprecated! Use `dbtc runs get` instead."""
    return get_run(ctx, account_id, run_id, include_related)


@runs_app.command("get")
def get_run(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    include_related: str = INCLUDE_RELATED,
):
    """Get run by ID for a specific account."""
    _dbt_cloud_request(
        ctx,
        "get_run",
        account_id,
        run_id,
        include_related=include_related,
    )


@app.command("get-run-artifact", hidden=True)
def get_run_artifact_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    path: str = typer.Option(
        ..., "--path", "-f", help="Name of artifact to retrieve (e.g. manifest.json)"
    ),
    step: int = typer.Option(
        None, "--step", "-s", help="Index of the step in the run to retrieve"
    ),
):
    """This will soon be deprecated! Use `dbtc runs get-artifact` instead."""
    return get_run_artifact(ctx, account_id, run_id, path, step)


@runs_app.command("get-artifact")
def get_run_artifact(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    path: str = typer.Option(
        ..., "--path", "-f", help="Name of artifact to retrieve (e.g. manifest.json)"
    ),
    step: int = typer.Option(
        None, "--step", "-s", help="Index of the step in the run to retrieve"
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
        "get_run_artifact",
        account_id=account_id,
        run_id=run_id,
        path=path,
        step=step,
    )


@app.command("get-run-timing-details", hidden=True)
def get_run_timing_details_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    run_id: int = RUN_ID,
):
    """This will soon be deprecated! Use `dbtc runs get-timing-details` instead."""
    return get_run_timing_details(ctx, account_id, project_id, run_id)


@runs_app.command("get-run-timing-details")
def get_run_timing_details(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    project_id: int = PROJECT_ID,
    run_id: int = RUN_ID,
):
    """Get run timing details for specific run."""
    _dbt_cloud_request(
        ctx,
        "get_run_timing_details",
        account_id,
        project_id,
        run_id,
    )


@app.command("list-run-artifacts", hidden=True)
def list_run_artifacts_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    step: int = typer.Option(None, "--step", "-s"),
):
    """This will soon be deprecated! Use `dbtc runs list-artifacts` instead."""
    return list_run_artifacts(ctx, account_id, run_id, step)


@runs_app.command("list-artifacts")
def list_run_artifacts(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    run_id: int = RUN_ID,
    step: int = typer.Option(None, "--step", "-s"),
):
    """List run artifacts

    Use this endpoint to fetch a list of artifact fiels generated for a completed run.

    !!! note
        By default, this endpoint returns artifacts from the last step in the run.
        To list artifacts from other steps in the run, use the `step` query parameter.
    """
    _dbt_cloud_request(ctx, "list_run_artifacts", account_id, run_id, step=step)


@app.command("list-runs", hidden=True)
def list_runs_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    include_related: str = INCLUDE_RELATED,
    job_id: int = typer.Option(
        None, "--job-id", "-j", help="Numeric ID of job to retrieve"
    ),
    environment_id: int = typer.Option(
        None, "--environment-id", "-e", help="Numeric ID of environment to retrieve"
    ),
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    deferring_run_id: int = typer.Option(
        None, "--deferring-run-id", help="The deferring run ID"
    ),
    status: str = typer.Option(
        None, "--status", help="Status to apply when listing runs"
    ),
    order_by: str = ORDER_BY,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """This will soon be deprecated! Use `dbtc runs list` instead."""
    return list_runs(
        ctx,
        account_id,
        include_related,
        job_id,
        environment_id,
        project_id,
        deferring_run_id,
        status,
        order_by,
        offset,
        limit,
    )


@runs_app.command("list")
def list_runs(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    include_related: str = INCLUDE_RELATED,
    job_id: int = typer.Option(
        None, "--job-id", "-j", help="Numeric ID of job to retrieve"
    ),
    environment_id: int = typer.Option(
        None, "--environment-id", "-e", help="Numeric ID of environment to retrieve"
    ),
    project_id: str = typer.Option(
        None, "--project-id", "-p", help="The project ID or IDs"
    ),
    deferring_run_id: int = typer.Option(
        None, "--deferring-run-id", help="The deferring run ID"
    ),
    status: str = typer.Option(
        None, "--status", help="Status to apply when listing runs"
    ),
    order_by: str = ORDER_BY,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """List of runs for a specific account."""
    if status is not None:
        try:
            status = json.loads(status)
        except ValueError:
            pass
    """List runs for a specific account."""
    _dbt_cloud_request(
        ctx,
        "list_runs",
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


# endregion

# region SERVICE_TOKENS


@app.command("assign-service-token-permissions", hidden=True)
def assign_service_token_permissions_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    service_token_id: int = SERVICE_TOKEN_ID,
    payload: str = PAYLOAD,
):
    """
    This will soon be deprecated! Use `dbtc service-tokens assign-permissions` instead.
    """
    return assign_service_token_permissions(ctx, account_id, service_token_id, payload)


@service_tokens_app.command("assign-permissions")
def assign_service_token_permissions(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    service_token_id: int = SERVICE_TOKEN_ID,
    payload: str = PAYLOAD,
):
    """Assign permissions to a service token."""
    _dbt_cloud_request(
        ctx,
        "assign_service_token_permissions",
        account_id,
        service_token_id,
        json.loads(payload),
    )


@app.command("create-service-token", hidden=True)
def create_service_token_old(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """This will soon be deprecated! Use `dbtc service-tokens create` instead."""
    return create_service_token(ctx, account_id, payload)


@service_tokens_app.command("create")
def create_service_token(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """Create a service token."""
    _dbt_cloud_request(ctx, "create_service_token", account_id, json.loads(payload))


@app.command("list-service-tokens-permissions", hidden=True)
def list_service_token_permissions_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    service_token_id: int = SERVICE_TOKEN_ID,
):
    """
    This will soon be deprecated! Use `dbtc service-tokens list-permissions` instead.
    """
    return list_service_token_permissions(ctx, account_id, service_token_id)


@service_tokens_app.command("list-permissions")
def list_service_token_permissions(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    service_token_id: int = SERVICE_TOKEN_ID,
):
    """List service token permissions for a specific account."""
    _dbt_cloud_request(
        ctx, "list_service_token_permissions", account_id, service_token_id
    )


# endregion

# region USERS


@app.command("deactivate-user-license", hidden=True)
def deactivate_user_license_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    permission_id: int = typer.Option(..., "--permission-id"),
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc users deactivate-license` instead."""
    return deactivate_user_license(ctx, account_id, permission_id, payload)


@users_app.command("deactivate")
def deactivate_user_license(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    permission_id: int = typer.Option(..., "--permission-id"),
    payload: str = PAYLOAD,
):
    """Deactive a user license."""
    _dbt_cloud_request(
        ctx, "deactivate_user_license", account_id, permission_id, json.loads(payload)
    )


@app.command("get-user", hidden=True)
def get_user_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    user_id: int = USER_ID,
):
    """This will soon be deprecated! Use `dbtc users get` instead."""
    return get_user(ctx, account_id, user_id)


@users_app.command("get")
def get_user(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    user_id: int = USER_ID,
):
    """Get a user."""
    _dbt_cloud_request(
        ctx,
        "get_user",
        account_id,
        user_id,
    )


@app.command("list-invited-users", hidden=True)
def list_invited_users_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
):
    """This will soon be deprecated! Use `dbtc users list-invited` instead."""
    return list_invited_users(ctx, account_id)


@users_app.command("list-invited")
def list_invited_users(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    """List invited users for a specific account."""
    _dbt_cloud_request(ctx, "list_invited_users", account_id)


@app.command("list-users", hidden=True)
def list_users_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    order_by: str = ORDER_BY,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """This will soon be deprecated! Use `dbtc users list` instead."""
    return list_users(ctx, account_id, order_by, offset, limit)


@users_app.command("list")
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
        "list_users",
        account_id,
        order_by=order_by,
        offset=offset,
        limit=limit,
    )


# endregion

# region WEBHOOKS


@app.command("create-webhook", hidden=True)
def create_webhook_old(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """This will soon be deprecated! Use `dbtc webhooks create` instead."""
    return create_webhook(ctx, account_id, payload)


@webhooks_app.command("create")
def create_webhook(
    ctx: typer.Context, account_id: int = ACCOUNT_ID, payload: str = PAYLOAD
):
    """Create a webhook."""
    _dbt_cloud_request(ctx, "create_webhook", account_id, json.loads(payload))


@app.command("delete-webhook", hidden=True)
def delete_webhook_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
):
    """This will soon be deprecated! Use `dbtc webhooks delete` instead."""
    return delete_webhook(ctx, account_id, webhook_id)


@webhooks_app.command("delete")
def delete_webhook(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
):
    """Delete a webhook."""
    _dbt_cloud_request(ctx, "delete_webhook", account_id, webhook_id)


@app.command("get-webhook", hidden=True)
def get_webhook_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
):
    """This will soon be deprecated! Use `dbtc webhooks get` instead."""
    return get_webhook(ctx, account_id, webhook_id)


@webhooks_app.command("get")
def get_webhook(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
):
    """Get a webhook by its ID"""
    _dbt_cloud_request(ctx, "get_webhook", account_id=account_id, webhook_id=webhook_id)


@app.command("list-webhooks", hidden=True)
def list_webhooks_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """This will soon be deprecated! Use `dbtc webhooks list` instead."""
    return list_webhooks(ctx, account_id, offset, limit)


@webhooks_app.command("list")
def list_webhooks(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    offset: int = OFFSET,
    limit: int = LIMIT,
):
    """List webhooks for a specific account."""
    _dbt_cloud_request(
        ctx,
        "list_webhooks",
        account_id,
        offset=offset,
        limit=limit,
    )


@app.command("test-webhook", hidden=True)
def test_webhook_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
):
    """This will soon be deprecated! Use `dbtc webhooks test` instead."""
    return test_webhook(ctx, account_id, webhook_id)


@webhooks_app.command("test")
def test_webhook(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
):
    """Test a webhook."""
    _dbt_cloud_request(
        ctx,
        "test_webhook",
        account_id,
        webhook_id,
    )


@app.command("update-webhook", hidden=True)
def update_webhook_old(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
    payload: str = PAYLOAD,
):
    """This will soon be deprecated! Use `dbtc webhooks update` instead."""
    return update_webhook(ctx, account_id, webhook_id, payload)


@webhooks_app.command("update")
def update_webhook(
    ctx: typer.Context,
    account_id: int = ACCOUNT_ID,
    webhook_id: str = WEBHOOK_ID,
    payload: str = PAYLOAD,
):
    """Update a webhook."""
    _dbt_cloud_request(
        ctx,
        "update_webhook",
        account_id,
        webhook_id,
        json.loads(payload),
    )


# endregion

# region METADATA


@metadata_app.command("column-lineage")
def column_lineage(
    ctx: typer.Context,
    environment_id: int = ENVIRONMENT_ID,
    node_unique_id: str = UNIQUE_ID,
    *,
    max_depth: int = typer.Option(
        None, "--max-depth", help="Maximum depth of the lineage graph."
    ),
    column_name: str = typer.Option(
        None, "--column-name", help="Name of the column to filter lineage for."
    ),
    is_error: bool = typer.Option(
        False, "--is-error", help="Whether to return only error nodes."
    ),
):
    _dbt_api_request(
        ctx,
        "metadata",
        "column_lineage",
        environment_id,
        node_unique_id,
        max_depth=max_depth,
        column_name=column_name,
        is_error=is_error,
    )


@metadata_app.command("longest-executed-models")
def longest_executed_models(
    ctx: typer.Context,
    environment_id: int = ENVIRONMENT_ID,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
    *,
    limit: int = typer.Option(5, "--limit", help="Maximum number of models to return."),
    job_limit: int = typer.Option(
        5, "--job-limit", help="Maximum number of jobs to return."
    ),
    order_by: str = typer.Option(
        "MAX", "--order-by", help="Order the results by MAX or AVG."
    ),
):
    _dbt_api_request(
        ctx,
        "metadata",
        "longest_executed_models",
        environment_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        job_limit=job_limit,
        order_by=order_by,
    )


@metadata_app.command("mesh-projects")
def mesh_projects(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    _dbt_api_request(
        ctx,
        "metadata",
        "mesh_projects",
        account_id,
    )


@metadata_app.command("model-execution-history")
def model_execution_history(
    ctx: typer.Context,
    environment_id: int = ENVIRONMENT_ID,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
    unique_id: str = UNIQUE_ID,
):
    _dbt_api_request(
        ctx,
        "metadata",
        "model_execution_history",
        environment_id,
        start_date=start_date,
        end_date=end_date,
        unique_id=unique_id,
    )


@metadata_app.command("model-job-information")
def model_job_information(
    ctx: typer.Context,
    environment_id: int = ENVIRONMENT_ID,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
    unique_id: str = UNIQUE_ID,
):
    _dbt_api_request(
        ctx,
        "metadata",
        "model_job_information",
        environment_id,
        start_date=start_date,
        end_date=end_date,
        unique_id=unique_id,
    )


@metadata_app.command("most-executed-models")
def most_executed_models(
    ctx: typer.Context,
    environment_id: int = ENVIRONMENT_ID,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
    *,
    limit: int = typer.Option(5, "--limit", help="Maximum number of models to return."),
    job_limit: int = typer.Option(
        5, "--job-limit", help="Maximum number of jobs to return."
    ),
):
    _dbt_api_request(
        ctx,
        "metadata",
        "most_executed_models",
        environment_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
        job_limit=job_limit,
    )


@metadata_app.command("most-failed-models")
def most_failed_models(
    ctx: typer.Context,
    environment_id: int = ENVIRONMENT_ID,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
    *,
    limit: int = typer.Option(5, "--limit", help="Maximum number of models to return."),
):
    _dbt_api_request(
        ctx,
        "metadata",
        "most_failed_models",
        environment_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )


@metadata_app.command("most-test-failures")
def most_models_test_failures(
    ctx: typer.Context,
    environment_id: int = ENVIRONMENT_ID,
    start_date: str = START_DATE,
    end_date: str = END_DATE,
    *,
    limit: int = typer.Option(5, "--limit", help="Maximum number of models to return."),
):
    _dbt_api_request(
        ctx,
        "metadata",
        "most_models_test_failures",
        environment_id,
        start_date=start_date,
        end_date=end_date,
        limit=limit,
    )


@metadata_app.command("public-models")
def public_models(ctx: typer.Context, account_id: int = ACCOUNT_ID):
    _dbt_api_request(
        ctx,
        "metadata",
        "public_models",
        account_id,
    )


@metadata_app.command("query")
def query(
    ctx: typer.Context,
    query: str = typer.Option(..., "--query", "-q", help="The GraphQL query to run."),
    variables: str = typer.Option(
        None, "--variables", help="The variables to include in the request."
    ),
    max_pages: int = typer.Option(
        None, "--max-pages", help="Maximum number of pages to retrieve."
    ),
    paginated_request_to_list: bool = typer.Option(
        True, "--to-list", help="Whether to convert paginated requests to a list."
    ),
):
    if variables is not None:
        variables = json.loads(variables)
    _dbt_api_request(
        ctx, "metadata", "query", query, variables, max_pages, paginated_request_to_list
    )


@metadata_app.command("recommendations")
def recommendations(
    ctx: typer.Context,
    environment_id: int = ENVIRONMENT_ID,
    *,
    first: int = typer.Option(
        500, "--first", help="Maximum number of items to return in a single request."
    ),
    severity: str = typer.Option(
        None, "--severity", help="Severity to filter recommendations by."
    ),
    categories: str = typer.Option(
        None, "--categories", help="Categories to filter recommendations by."
    ),
    rule_names: str = typer.Option(
        None, "--rule-names", help="Rules to filter recommendations by."
    ),
    unique_ids: str = typer.Option(
        None, "--unique-ids", help="Unique IDs to filter recommendations by."
    ),
):
    def _to_list(value):
        if value is None:
            return None

        try:
            return json.loads(value)

        except ValueError:
            return value

    _dbt_api_request(
        ctx,
        "metadata",
        "recommendations",
        environment_id,
        first=first,
        severity=_to_list(severity),
        categories=_to_list(categories),
        rule_names=_to_list(rule_names),
        unique_ids=_to_list(unique_ids),
    )


# endregion


def main():
    app()
