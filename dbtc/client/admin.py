# stdlib
import enum
import json
import time
from datetime import datetime
from functools import partial, wraps
from typing import Dict, List, Optional, Union

# third party
import requests

# first party
from dbtc import models
from dbtc.client.base import _Client
from dbtc.utils import json_listify, listify


class JobRunStatus(enum.IntEnum):
    QUEUED = 1
    STARTING = 2
    RUNNING = 3
    SUCCESS = 10
    ERROR = 20
    CANCELLED = 30


PULL_REQUESTS = (
    "github_pull_request_id",
    "gitlab_merge_request_id",
    "azure_pull_request_id",
)


def _version_decorator(func, version):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        self._path = f"/api/{version}/"
        result = func(self, *args, **kwargs)
        return result

    return wrapper


v2 = partial(_version_decorator, version="v2")
v3 = partial(_version_decorator, version="v3")


class _AdminClient(_Client):
    def __init__(self, session, **kwargs):
        super().__init__(session, **kwargs)

    _path = None

    @property
    def _header_property(self):
        if self.api_key is None:
            return "service_token"

        return "api_key"

    def _make_request(
        self, path: str, *, method: str = "get", **kwargs
    ) -> requests.Response:
        """Make request to API."""

        # Model is not an argument that the request method accepts, needs to be removed
        model = kwargs.pop("model", None)
        if model is not None:
            # This will validate the payload
            kwargs["json"] = model(**kwargs["json"]).model_dump(exclude_unset=True)

        full_url = self.full_url(path)
        response = self.session.request(method=method, url=full_url, **kwargs)
        return response

    def _simple_request(self, path: str, *, method: str = "get", **kwargs) -> Dict:
        """Return json from response."""
        response = self._make_request(path, method=method, **kwargs)
        return response.json()

    def _get_by_name(self, items: List, item_name: str, value: str = "name"):
        try:
            obj = [item for item in items if item[value] == item_name][0]
        except IndexError:
            obj = None
        return obj

    # ADAPTERS

    @v3
    def create_adapter(self, account_id: int, project_id: int, payload: Dict) -> Dict:
        """Create an adapter

        !!! note
            This is a prerequisite for creating a Databricks connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the adapter to create
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/adapters/",
            method="post",
            json=payload,
        )

    @v3
    def delete_adapter(self, account_id: int, project_id: int, adapter_id: int) -> Dict:
        """Delete an adapter

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            adapter_id (int): Numeric ID of the adapter to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/adapters/{adapter_id}/",
            method="delete",
        )

    @v3
    def get_adapter(self, account_id: int, project_id: int, adapter_id: int) -> Dict:
        """Get an adapter

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            adapter_id (int): Numeric ID of the adapter
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/adapters/{adapter_id}/",
        )

    @v3
    def update_adapter(
        self, account_id: int, project_id: int, adapter_id: int, payload: Dict
    ) -> Dict:
        """Update an adapter

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            adapter_id (int): Numeric ID of the adapter
            payload (dict): Dictionary representing the adapter to update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/adapters/{adapter_id}/",
            method="post",
            json=payload,
        )

    # AUDIT LOGS

    @v3
    def list_audit_logs(
        self,
        account_id: int,
        *,
        logged_at_start: str = None,
        logged_at_end: str = None,
        offset: int = None,
        limit: int = None,
    ) -> Dict:
        """List audit logs for a specific account

        !!! note
            This API is only available to enterprise customers.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            logged_at_start (str, optional):  Date to begin retrieving audit
                logs
                Format is yyyy-mm-dd
            logged_at_end (str, optional): Date to stop retrieving audit logs.
                Format is yyyy-mm-dd
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
        """
        return self._simple_request(
            f"accounts/{account_id}/audit-logs",
            params={
                "logged_at_start": logged_at_start,
                "logged_at_end": logged_at_end,
                "offset": offset,
                "limit": limit,
            },
        )

    # CONNECTIONS

    @v3
    def create_connection(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the connection to create
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/connections/",
            method="post",
            json=payload,
        )

    @v3
    def delete_connection(
        self, account_id: int, project_id: int, connection_id: int
    ) -> Dict:
        """Delete a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            connection_id (int): Numeric ID of the connection to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/connections/{connection_id}",
            method="delete",
        )

    @v3
    def get_connection(
        self, account_id: int, project_id: int, connection_id: int
    ) -> Dict:
        """Get a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            connection_id (int): Numeric ID of the connection to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/connections/{connection_id}",
        )

    @v3
    def list_connections(
        self,
        account_id: int,
        project_id: int,
        *,
        state: int = None,
        offset: int = None,
        limit: int = None,
    ) -> Dict:
        """List connections for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
            state (int, optional): 1 = active, 2 = deleted
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/connections",
            params={"state": state, "limit": limit, "offset": offset},
        )

    @v3
    def update_connection(
        self, account_id: int, project_id: int, connection_id: int, payload: Dict
    ) -> Dict:
        """Update a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            connection_id (int): Numeric ID of the connection to update
            payload (dict): Dictionary representing the connection to update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/connections/{connection_id}/",
            method="post",
            json=payload,
        )

    # CREDENTIALS

    @v3
    def create_credentials(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create credentials

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the credentials to create
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/credentials/",
            method="post",
            json=payload,
        )

    @v3
    def delete_credentials(
        self, account_id: int, project_id: int, credentials_id: int
    ) -> Dict:
        """Delete credentials

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            credentials_id (int): Numeric ID of the credentials to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/credentials/{credentials_id}/",  # noqa: E501
            method="delete",
        )

    @v3
    def get_credentials(
        self, account_id: int, project_id: int, credentials_id: int
    ) -> Dict:
        """Get credentials

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            credentials_id (int): Numeric ID of the credentials to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/credentials/{credentials_id}/",  # noqa: E501
        )

    @v3
    def list_credentials(self, account_id: int, project_id: int) -> Dict:
        """List credentials for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/credentials"
        )

    @v3
    def partial_update_credentials(
        self, account_id: int, project_id: int, credentials_id: int, payload: Dict
    ) -> Dict:
        """Partial update credentials

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            credentials_id (int): Numeric ID of the credentials to update
            payload (dict): Dictionary representing the credentials to update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/credentials/{credentials_id}/",  # noqa: E501
            method="patch",
            json=payload,
        )

    @v3
    def update_credentials(
        self, account_id: int, project_id: int, credentials_id: int, payload: Dict
    ) -> Dict:
        """Update credentials

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            credentials_id (int): Numeric ID of the credentials to update
            payload (dict): Dictionary representing the credentials to update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/credentials/{credentials_id}/",  # noqa: E50
            method="post",
            json=payload,
        )

    # ENV VARS

    @v3
    def create_env_vars(self, account_id: int, project_id: int, payload: Dict) -> Dict:
        """Create environment variables

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the environment variables to create
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environment-variables/",
            method="post",
            json=payload,
        )

    @v3
    def create_env_vars_bulk(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create environment variables in bulk

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the environment variables to create
                in bulk
        """
        url = f"accounts/{account_id}/projects/{project_id}/environment-variables/bulk/"
        return self._simple_request(url, method="post", json=payload)

    @v3
    def delete_env_vars(
        self, account_id: int, project_id: int, env_var_id: int
    ) -> Dict:
        """Delete environment variables

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            env_var_id (int): Numeric ID of the environment variable to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environment-variables/{env_var_id}/",  # noqa: E501
            method="delete",
        )

    @v3
    def delete_env_vars_bulk(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Delete environment variables in bulk

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the environment variables to delete
                in bulk
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environment-variables/bulk/",
            method="delete",
            json=payload,
        )

    @v3
    def list_environment_variables(
        self,
        account_id: int,
        project_id: int,
        *,
        resource_type: str = "environment",
        environment_id: int = None,
        job_id: int = None,
        limit: int = None,
        offset: int = None,
        name: str = None,
        state: int = None,
        type: str = None,
        user_id: int = None,
    ):
        """List environment variables for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of he project to retrieve
            resource_type (str, optional): The name of the resource to retrieve. Valid
                resources include environment, job, and user
            environment_id (int, optional): Numeric ID of the environment to retrieve
            job_id (int, optional): Numeric ID of the job to retrieve
            name (str, optional): Name of the environment to retrieve
            type (str, optional): Type of the environment variable
            state (int, optional): 1 = active, 2 = deleted
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
        """
        valid_resource_types = ["environment", "job", "user"]
        if resource_type not in valid_resource_types:
            raise ValueError(
                f"{resource_type} is not a valid argument for resource_type.  Valid "
                f'resource types include {", ".join(valid_resource_types)}.'
            )

        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environment-variables/{resource_type}",  # noqa: E501
            params={
                "environment_id": environment_id,
                "job_definition_id": job_id,
                "name": name,
                "type": type,
                "state": state,
                "offset": offset,
                "limit": limit,
                "user_id": user_id,
            },
        )

    @v3
    def update_env_vars(
        self, account_id: int, project_id: int, env_var_id: int, payload: Dict
    ) -> Dict:
        """Update environment variables

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            env_var_id (int): Numeric ID of the environment variable to update
            payload (dict): Dictionary representing the environment variables to update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environment-variables/{env_var_id}/",  # noqa: E501
            method="post",
            json=payload,
        )

    @v3
    def update_env_vars_bulk(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Update environment variables in bulk

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the environment variables to update
                in bulk
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environment-variables/bulk/",
            method="post",
            json=payload,
        )

    # ENVIRONMENTS

    @v3
    def create_environment(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create an environment

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the environment to create
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environments/",
            method="post",
            json=payload,
        )

    @v3
    def delete_environment(self, account_id: int, environment_id: int) -> Dict:
        """Delete job for a specified account

        Args:
            account_id (int): Numeric ID of the account
            environment_id (int): Numeric ID of the environment to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/environments/{environment_id}/",
            method="delete",
        )

    @v3
    def get_environment(
        self, account_id: int, project_id: int, environment_id: int
    ) -> Dict:
        """Get an environment by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
            environment_id (int): Numeric ID of the environment to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environments/{environment_id}"
        )

    @v3
    def list_environments(
        self,
        account_id: int,
        project_id: int,
        *,
        dbt_version: Union[str, List[str]] = None,
        deployment_type: Union[str, List[str]] = None,
        credentials_id: int = None,
        name: str = None,
        type: str = None,
        state: int = None,
        offset: int = None,
        limit: int = None,
        order_by: str = None,
    ) -> Dict:
        """List environments for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int or list, optional): The project ID or IDs
            dbt_version (str or list, optional): The version of dbt the environment
                is using
            deployment_type (str or list, optional): The deployment type of the
                environment. Valid values are "staging" and "production"
            credentials_id (int, optional): Numeric ID of the credentials to retrieve
            name (str, optional): Name of the environment to retrieve
            type (str, optional): Type of the environment (deployment or development)
            state (int, optional): 1 = active, 2 = deleted
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
            order_by (str, optional): Field to order the result by.
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environments/",
            params={
                "dbt_version__in": json_listify(dbt_version),
                "deployment_type__in": json_listify(deployment_type),
                "credentials_id": credentials_id,
                "name": name,
                "type": type,
                "state": state,
                "offset": offset,
                "limit": limit,
                "order_by": order_by,
            },
        )

    @v3
    def update_environment(
        self, account_id: int, project_id: int, environment_id: int, payload: Dict
    ) -> Dict:
        """Update a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            environment_id (int): Numeric ID of the environment to update
            payload (dict): Dictionary representing the environment to update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environments/{environment_id}/",  # noqa: E501
            method="post",
            json=payload,
        )

    # EXTENDED ATTRIBUTES

    @v3
    def create_extended_attributes(self, account_id: int, project_id: int) -> Dict:
        """Create a new Extended Attributes record

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/extended-attributes/",
            method="post",
        )

    @v3
    def delete_extended_attributes(
        self, account_id: int, project_id: int, extended_attributes_id: int
    ) -> Dict:
        """Delete an Extended Attributes record

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            extended_attributes_id (int): Numeric ID of the extended attributes record
                to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/extended-attributes/{extended_attributes_id}/",  # noqa: E501
            method="delete",
        )

    @v3
    def get_extended_attributes(
        self, account_id: int, project_id: int, extended_attributes_id: int
    ) -> Dict:
        """Get an Extended Attributes record

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            extended_attributes_id (int): Numeric ID of the extended attributes record
                to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/extended-attributes/{extended_attributes_id}/",  # noqa: E501
        )

    @v3
    def update_extended_attributes(
        self,
        account_id: int,
        project_id: int,
        extended_attributes_id: int,
        payload: Dict,
    ) -> Dict:
        """Update an Extended Attributes record

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            extended_attributes_id (int): Numeric ID of the extended attributes record
                to update
            payload (dict): Dictionary representing the extended attributes record to
                update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/extended-attributes/{extended_attributes_id}/",  # noqa: E501
            method="post",
            json=payload,
        )

    # GROUPS

    @v3
    def assign_group_permissions(
        self, account_id: int, group_id: int, payload: Dict
    ) -> Dict:
        """Assign group permissions

        Args:
            account_id (int): Numeric ID of the account
            group_id (int): Numeric ID of the group
            payload (dict): Dictionary representing the group to create
        """
        return self._simple_request(
            f"accounts/{account_id}/group-permissions/{group_id}/",
            method="post",
            json=payload,
        )

    @v3
    def assign_project_group_permissions(self, account_id: int, project_id: int):
        """Assign project group permissions

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the project group permissions to
                assign
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/group-permissions/",
            method="post",
        )

    @v3
    def assign_user_to_group(self, account_id: int, payload: Dict) -> Dict:
        """Assign a user to a group

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the user to assign
            {
                "user_id": int,
                "desired_group_ids": list(int)
            }
        """
        return self._simple_request(
            f"accounts/{account_id}/assign-groups/",
            method="post",
            json=payload,
        )

    @v3
    def create_group(self, account_id: int, payload: Dict) -> Dict:
        """Create a group

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the group to create
        """
        return self._simple_request(
            f"accounts/{account_id}/groups/", method="post", json=payload
        )

    @v3
    def get_group(self, account_id: int, group_id: int) -> Dict:
        """Get a group

        Args:
            account_id (int): Numeric ID of the account
            group_id (int): Numeric ID of the group
        """
        return self._simple_request(
            f"accounts/{account_id}/groups/{group_id}/",
        )

    @v3
    def list_groups(self, account_id: int) -> Dict:
        """List groups for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/groups/")

    @v3
    def update_group(self, account_id: int, group_id: int, payload: Dict) -> Dict:
        """Update a group

        Args:
            account_id (int): Numeric ID of the account
            group_id (int): Numeric ID of the group
            payload (dict): Dictionary representing the group to update
        """
        return self._simple_request(
            f"accounts/{account_id}/groups/{group_id}/",
            method="post",
            json=payload,
        )

    # LICENSE MAPS

    @v3
    def create_license_map(self, account_id: int, payload: Dict) -> Dict:
        """Create a license map

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the license map to create
        """
        return self._simple_request(
            f"accounts/{account_id}/license-maps/",
            method="post",
            json=payload,
        )

    @v3
    def delete_license_map(self, account_id: int, license_map_id: int) -> Dict:
        """Delete a license map

        Args:
            account_id (int): Numeric ID of the account
            license_map_id (int): Numeric ID of the license map to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/license-maps/{license_map_id}/",
            method="delete",
        )

    @v3
    def get_license_map(self, account_id: int, license_map_id: int) -> Dict:
        """Get a license map

        Args:
            account_id (int): Numeric ID of the account
            license_map_id (int): Numeric ID of the license map
        """
        return self._simple_request(
            f"accounts/{account_id}/license-maps/{license_map_id}/",
        )

    @v3
    def list_license_maps(self, account_id: int) -> Dict:
        """List license maps for a specific account

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/license-maps/")

    @v3
    def update_license_map(
        self, account_id: int, license_map_id: int, payload: Dict
    ) -> Dict:
        """Update a license map

        Args:
            account_id (int): Numeric ID of the account
            license_map_id (int): Numeric ID of the license map
            payload (dict): Dictionary representing the license map to update
        """
        return self._simple_request(
            f"accounts/{account_id}/license-maps/{license_map_id}/",
            method="post",
            json=payload,
        )

    # PRIVATE LINK

    @v3
    def list_private_link_endpoints(self, account_id: int) -> Dict:
        """List private link endpoints for a specific account

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/private-link-endpoints/")

    # PROJECTS

    @v3
    def create_project(self, account_id: int, payload: Dict) -> Dict:
        """Create a project

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the project to create
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/", method="post", json=payload
        )

    @v3
    def delete_project(self, account_id: int, project_id: int) -> Dict:
        """Delete project for a specified account

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/",
            method="delete",
        )

    @v3
    def get_project(self, account_id: int, project_id: int) -> Dict:
        """Get a project by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/projects/{project_id}")

    @v3
    def get_project_by_name(
        self, project_name: str, account_id: int = None, account_name: str = None
    ) -> Dict:
        """Get a project by its name.

        Args:
            project_name (str): Name of project to retrieve
            account_id (int, optional): Numeric ID of the account to retrieve
            account_name (str, optional): Name of account to retrieve
        """
        if account_id is None and account_name is None:
            accounts = self.list_accounts()
            for account in accounts["data"]:
                projects = self.list_projects(account["id"])
                project = self._get_by_name(projects["data"], project_name)
                if project is not None:
                    break

        else:
            if account_id is not None:
                account = self.get_account(account_id)
            else:
                account = self.get_account_by_name(account_name)
            if account.get("data", None) is not None:
                projects = self.list_projects(account["data"]["id"])
                project = self._get_by_name(projects["data"], project_name)
            else:
                project = None

        if project is not None:
            return self.get_project(project["account_id"], project["id"])

        raise Exception(f'Project "{project_name}" was not found.')

    @v3
    def list_projects(
        self,
        account_id: int,
        *,
        project_id: Union[int, List[int]] = None,
        state: int = None,
        offset: int = None,
        limit: int = None,
    ) -> Dict:
        """List projects for a specified account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int or list, optional): The project ID or IDs
            state (int, optional): 1 = active, 2 = deleted
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
        """
        return self._simple_request(
            f"accounts/{account_id}/projects",
            params={
                "pk__in": json_listify(project_id),
                "state": state,
                "offset": offset,
                "limit": limit,
            },
        )

    @v3
    def update_project(self, account_id: int, project_id: int, payload: Dict) -> Dict:
        """Update project for a specified account

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project to update
            payload (dict): Dictionary representing the project to update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/", method="POST", json=payload
        )

    # REPOS

    @v3
    def create_managed_repository(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create a new dbt Cloud managed repository

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/managed-repositories/",
            method="post",
            json=payload,
        )

    @v3
    def create_repository(
        self, account_id: int, project_id: int, payload: Dict
    ) -> Dict:
        """Create a repository

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the repository to create

        !!! note
            After creating / updating a dbt Cloud repository's SSH key, you will need
            to add the generated key text as a deploy key to the target repository.
            This gives dbt Cloud permissions to read / write in the repository

            You can read more in the [docs](https://docs.getdbt.com/docs/dbt-cloud/cloud-configuring-dbt-cloud/cloud-configuring-repositories)  # noqa: E501
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/repositories/",
            method="post",
            json=payload,
        )

    @v3
    def delete_repository(
        self, account_id: int, project_id: int, repository_id: int
    ) -> Dict:
        """Delete repository for a specified account

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            repository_id (int): Numeric ID of the repository to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/repositories/{repository_id}",
            method="delete",
        )

    @v3
    def get_repository(
        self, account_id: int, project_id: int, repository_id: int
    ) -> Dict:
        """Get a repository by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
            repository_id (int): Numeric ID of the repository to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/repositories/{repository_id}"
        )

    @v3
    def list_repositories(self, account_id: int, project_id: int) -> Dict:
        """List repositories for a specific account and project

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/repositories/"
        )

    @v3
    def update_repository(
        self, account_id: int, project_id: int, repository_id: int, payload: Dict
    ) -> Dict:
        """Update a connection

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            repository_id (int): Numeric ID of the repository to update
            payload (dict): Dictionary representing the repository to update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/repositories/{repository_id}/",  # noqa: E501
            method="post",
            json=payload,
        )

    # SEMANTIC LAYER CONFIG

    @v3
    def create_sl_config(self, account_id: int, project_id: int, payload: Dict) -> Dict:
        """Create a semantic layer configuration

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the semantic layer configuration to
                create
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/semantic-layer-configurations",  # noqa: E501
            method="post",
            json=payload,
        )

    @v3
    def delete_sl_config(
        self, account_id: int, project_id: int, sl_config_id: int
    ) -> Dict:
        """Delete a semantic layer configuration

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            sl_config_id (int): Numeric ID of the semantic layer configuration to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/semantic-layer-configurations/{sl_config_id}",  # noqa: E501
            method="delete",
        )

    @v3
    def get_sl_config(
        self, account_id: int, project_id: int, sl_config_id: int
    ) -> Dict:
        """Get a semantic layer configuration by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
            sl_config_id (int): Numeric ID of the semantic layer configuration to
                retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/semantic-layer-configurations/{sl_config_id}"  # noqa: E501
        )

    @v3
    def update_sl_config(
        self, account_id: int, project_id: int, sl_config_id: int, payload: Dict
    ) -> Dict:
        """Update a semantic layer configuration

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            sl_config_id (int): Numeric ID of the semantic layer configuration to update
            payload (dict): Dictionary representing the semantic layer configuration to
                update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/semantic-layer-configurations/{sl_config_id}",  # noqa: E501
            method="post",
            json=payload,
        )

    # SEMANTIC LAYER CREDS

    @v3
    def create_sl_creds(self, account_id: int, project_id: int, payload: Dict) -> Dict:
        """Create a semantic layer credential

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the semantic layer credential to
                create
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/semantic-layer-credentials",
            method="post",
            json=payload,
        )

    @v3
    def delete_sl_creds(
        self, account_id: int, project_id: int, sl_creds_id: int
    ) -> Dict:
        """Delete a semantic layer credential

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            sl_creds_id (int): Numeric ID of the semantic layer credential to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/semantic-layer-credentials/{sl_creds_id}",  # noqa: E501
            method="delete",
        )

    @v3
    def get_sl_creds(self, account_id: int, project_id: int, sl_creds_id: int) -> Dict:
        """Get a semantic layer credential by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            project_id (int): Numeric ID of the project to retrieve
            sl_creds_id (int): Numeric ID of the semantic layer credential to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/semantic-layer-credentials/{sl_creds_id}"  # noqa: E501
        )

    @v3
    def partially_update_sl_creds(
        self, account_id: int, project_id: int, sl_creds_id: int, payload: Dict
    ) -> Dict:
        """Partially update a semantic layer credential

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            sl_creds_id (int): Numeric ID of the semantic layer credential to update
            payload (dict): Dictionary representing the semantic layer credential to
                update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/semantic-layer-credentials/{sl_creds_id}",  # noqa: E501
            method="patch",
            json=payload,
        )

    @v3
    def update_sl_creds(
        self, account_id: int, project_id: int, sl_creds_id: int, payload: Dict
    ) -> Dict:
        """Update a semantic layer credential

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            sl_creds_id (int): Numeric ID of the semantic layer credential to update
            payload (dict): Dictionary representing the semantic layer credential to
                update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/semantic-layer-credentials/{sl_creds_id}",  # noqa: E501
            method="post",
            json=payload,
        )

    # SERVICE TOKENS

    @v3
    def assign_service_token_permissions(
        self, account_id: int, service_token_id: int, payload: List[Dict]
    ) -> Dict:
        """Assign permissions to a service token.

        Args:
            account_id (int): Numeric ID of the account
            service_token_id (int): Numeric ID of the service token
            payload (list): List of dictionaries representing the permissions to assign
        """
        return self._simple_request(
            f"accounts/{account_id}/service-tokens/{service_token_id}/permissions/",
            method="post",
            json=payload,
        )

    @v3
    def create_service_token(self, account_id: int, payload: Dict) -> Dict:
        """Create a service token

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the service token to create

        !!! note
            This request creates a service token, but does not assign permissions to
            it.  Permissions are assigned via the
            [assign_service_token_permissions](cloud.md#assign_service_token_permissions)

            See the [user tokens](https://docs.getdbt.com/docs/dbt-cloud/dbt-cloud-api/user-tokens)  # noqa: E501
            and [service tokens](https://docs.getdbt.com/docs/dbt-cloud/dbt-cloud-api/service-tokens)  # noqa: E501
            documentation for more information.
        """
        return self._simple_request(
            f"accounts/{account_id}/service-tokens/", method="post", json=payload
        )

    @v3
    def get_service_token(self, account_id: int, service_token_id: int) -> Dict:
        """Retrieves a service token.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            service_token_id (int): Numeric ID of the service token to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/service-tokens/{service_token_id}"
        )

    @v3
    def list_service_tokens(self, account_id: int) -> Dict:
        """List service tokens for a specific account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/service-tokens/")

    @v3
    def list_service_token_permissions(
        self, account_id: int, service_token_id: int
    ) -> Dict:
        """List service token permissions for a specific account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            service_token_id (int): Numeric ID of the service token to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/service-tokens/{service_token_id}/permissions"
        )

    @v2
    def cancel_run(self, account_id: int, run_id: int) -> Dict:
        """Cancel a run.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/runs/{run_id}/cancel",
            method="post",
        )

    @v2
    def create_job(self, account_id: int, payload: Dict) -> Dict:
        """Create a job

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the job to create
        """
        return self._simple_request(
            f"accounts/{account_id}/jobs/",
            method="post",
            json=payload,
        )

    @v3
    def create_webhook(self, account_id: int, payload: Dict) -> Dict:
        """Create a new outbound webhook

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the webhook to create
        """
        return self._simple_request(
            f"accounts/{account_id}/webhooks/subscriptions",
            method="post",
            json=payload,
            model=models.Webhook,
        )

    @v3
    def create_user_group(self, account_id: int, payload: Dict) -> Dict:
        """Create a user group

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the group to create

        !!! note
            The group_name is the name of the dbt Cloud group. The list of
            sso_mapping_groups are string values that dbt Cloud will attempt to match
            with incoming information from your identity provider at login time, in
            order to assign the group with group_name to the user.
        """
        return self._simple_request(
            f"accounts/{account_id}/groups/", method="post", json=payload
        )

    @v2
    def deactivate_user_license(
        self, account_id: int, permission_id: int, payload: Dict
    ) -> Dict:
        """Deactivate user license

        Args:
            account_id (int): Numeric ID of the account
            permission_id (int): Numeric ID of the permission that contains
                user you'd like to deactivate

        !!! note
            Ensure the `groups` object contains all of a user's assigned group
            permissions. This request will fail if a user has already been deactivated.
        """
        return self._simple_request(
            f"accounts/{account_id}/permissions/{permission_id}",
            method="post",
            json=payload,
        )

    @v2
    def delete_job(self, account_id: int, job_id: int) -> Dict:
        """Delete job for a specified account

        Args:
            account_id (int): Numeric ID of the account
            job_id (int): Numeric ID of the project to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/jobs/{job_id}/",
            method="delete",
        )

    @v3
    def delete_webhook(self, account_id: int, webhook_id: str) -> Dict:
        """Delete a webhook

        Args:
            account_id (int): Numeric ID of the account
            webhook_id (str): String ID of the webhook you want to delete
        """
        return self._simple_request(
            f"accounts/{account_id}/webhooks/subscription/{webhook_id}",
            method="delete",
        )

    @v3
    def delete_user_group(self, account_id: int, group_id: int, payload: Dict) -> Dict:
        """Delete group for a specified account

        Args:
            account_id (int): Numeric ID of the account
            group_id (int): Numeric ID of the group to delete
            payload (dict): Dictionary representing the group to delete with the format
                {
                    "account_id": int,
                    "name": str,
                    "id": int,
                    "state":2,
                    "assign_by_default":false,
                    "sso_mapping_groups": list
                }
        """
        return self._simple_request(
            f"accounts/{account_id}/groups/{group_id}/", method="post", payload=payload
        )

    @v2
    def get_account(self, account_id: int) -> Dict:
        """Get an account by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f"accounts/{account_id}")

    @v2
    def get_account_by_name(self, account_name: str) -> Dict:
        """Get an account by its name.

        Args:
            account_name (str): Name of an account
        """
        accounts = self.list_accounts()
        account = self._get_by_name(accounts["data"], account_name)
        if account is not None:
            return self.get_account(account["id"])

        raise Exception(f'Account "{account_name}" was not found')

    @v2
    def get_account_licenses(self, account_id: int) -> Dict:
        """List account licenses for a specified account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/licenses")

    @v2
    def get_job(self, account_id: int, job_id: int, *, order_by: str = None) -> Dict:
        """Get a job by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to retrieve
            order_by (str, optional): Field to order the result by.
                Use - to indicate reverse order.
        """
        return self._simple_request(
            f"accounts/{account_id}/jobs/{job_id}/",
            params={"order_by": order_by},
        )

    @v2
    def get_most_recent_run(
        self,
        account_id: int,
        *,
        include_related: List[str] = None,
        job_definition_id: int = None,
        environment_id: int = None,
        project_id: int = None,
        deferring_run_id: int = None,
        status: Union[List[str], str] = None,
    ) -> Dict:
        """Get the most recent run

        Args:
            account_id (int): Numeric ID of the account to retrieve
            include_related (list): List of related
                fields to pull with the run. Valid values are `trigger`, `job`,
                `repository`, `debug_logs`, `run_steps`, and `environment`.
            job_definition_id (int, optional): Applies a filter to only return
                runs from the specified Job.
            environment_id (int, optional): Numeric ID of the environment
            project_id (int or list, optional): The project ID or IDs
            deferring_run_id (int, optional): Numeric ID of a deferred run
            status (str or list, optional): The status to apply when listing runs.
                Options include queued, starting, running, success, error, and
                cancelled
        """
        runs = self.list_runs(
            account_id,
            include_related=include_related,
            job_definition_id=job_definition_id,
            environment_id=environment_id,
            project_id=project_id,
            deferring_run_id=deferring_run_id,
            order_by="-id",
            limit=1,
            status=status,
        )
        try:
            runs["data"] = runs.get("data", [])[0]
        except IndexError:
            runs["data"] = {}
        except TypeError:
            return runs

        return runs

    @v2
    def get_most_recent_run_artifact(
        self,
        account_id: int,
        path: str,
        *,
        job_definition_id: int = None,
        environment_id: int = None,
        project_id: int = None,
        deferring_run_id: int = None,
        step: int = None,
    ):
        """Fetch artifacts from the most recent run

        Once a run has completed, you can use this endpoint to download the
        `manifest.json`, `run_results.json` or `catalog.json` files from dbt Cloud.
        These artifacts contain information about the models in your dbt project,
        timing information around their execution, and a status message indicating the
        result of the model build.

        !!! note
            By default, this endpoint returns artifacts from the last step in the
            run. To list artifacts from other steps in the run, use the step query
            parameter described below.

        !!! warning
            If requesting a non JSON artifact, the result will be a `str`

        Args:
            account_id (int): Numeric ID of the account to retrieve
            path (str): Paths are rooted at the target/ directory. Use manifest.json,
                catalog.json, or run_results.json to download dbt-generated artifacts
                for the run.
            job_definition_id (int, optional): Applies a filter to only return
                runs from the specified Job.
            environment_id (int, optional): Numeric ID of the environment
            project_id (int or list, optional): The project ID or IDs
            deferring_run_id (int, optional): Numeric ID of a deferred run
            step (str, optional): The index of the Step in the Run to query for
                artifacts. The first step in the run has the index 1. If the step
                parameter is omitted, then this endpoint will return the artifacts
                compiled for the last step in the run.
        """
        runs = self.get_most_recent_run(
            account_id,
            job_definition_id=job_definition_id,
            environment_id=environment_id,
            project_id=project_id,
            deferring_run_id=deferring_run_id,
            status="success",
        )

        try:
            run_id = runs.get("data", {})["id"]
        except (TypeError, KeyError):
            return runs
        else:
            return self.get_run_artifact(account_id, run_id, path, step=step)

    @v2
    def get_run(
        self, account_id: int, run_id: int, *, include_related: List[str] = None
    ) -> Dict:
        """Get a run by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
            include_related (list): List of related
                fields to pull with the run. Valid values are `trigger`, `job`,
                `repository`, `debug_logs`, `run_steps`, and `environment`.
        """
        return self._simple_request(
            f"accounts/{account_id}/runs/{run_id}",
            params={"include_related": ",".join(include_related or [])},
        )

    @v2
    def get_run_artifact(
        self,
        account_id: int,
        run_id: int,
        path: str,
        *,
        step: int = None,
    ) -> Union[str, Dict]:
        """Fetch artifacts from a completed run.

        Once a run has completed, you can use this endpoint to download the
        `manifest.json`, `run_results.json` or `catalog.json` files from dbt Cloud.
        These artifacts contain information about the models in your dbt project,
        timing information around their execution, and a status message indicating the
        result of the model build.

        !!! note
            By default, this endpoint returns artifacts from the last step in the
            run. To list artifacts from other steps in the run, use the step query
            parameter described below.

        !!! warning
            If requesting a non JSON artifact, the result will be a `str`

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
            path (str): Paths are rooted at the target/ directory. Use manifest.json,
                catalog.json, or run_results.json to download dbt-generated artifacts
                for the run.
            step (str, optional): The index of the Step in the Run to query for
                artifacts. The first step in the run has the index 1. If the step
                parameter is omitted, then this endpoint will return the artifacts
                compiled for the last step in the run.
        """
        url_path = f"accounts/{account_id}/runs/{run_id}/artifacts/{path}"
        params = {"step": step}
        if path[-5:] == ".json":
            return self._simple_request(url_path, params=params)

        response = self._make_request(url_path, params=params)
        return response.text

    @v3
    def get_run_timing_details(
        self, account_id: int, project_id: int, run_id: int
    ) -> Dict:
        """Retrieves the timing details related to a run

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/runs/{run_id}/timing/"
        )

    @v3
    def get_webhook(self, account_id: int, webhook_id: str) -> Dict:
        """Get a webhook

        Args:
            account_id (int): Numeric ID of the account
            webhook_id (str): String ID of the webhook you want to retrieve
        """
        return self._simple_request(
            f"accounts/{account_id}/webhooks/subscription/{webhook_id}",
        )

    @v2
    def get_user(self, account_id: int, user_id: int) -> Dict:
        """List invited users in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            user_id (int): Numeric ID of the user to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/users/{user_id}/")

    @v3
    def list_accounts(self) -> Dict:
        """List of accounts that your API Token is authorized to access."""
        return self._simple_request("accounts/")

    @v3
    def list_environments_by_account(self, account_id: int) -> Dict:
        """List environments for a specific account

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/environments/")

    @v3
    def list_feature_flags(self, account_id: int) -> Dict:
        """List feature flags for a specific account

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/feature-flag/")

    @v2
    def list_invited_users(self, account_id: int) -> Dict:
        """List invited users in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
        """
        return self._simple_request(f"accounts/{account_id}/invites/")

    @v2
    def list_jobs(
        self,
        account_id: int,
        *,
        environment_id: int = None,
        project_id: Union[int, List[int]] = None,
        state: int = None,
        offset: int = None,
        limit: int = None,
        order_by: str = None,
    ) -> Dict:
        """List jobs in an account or specific project.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            environment_id (int): Numeric ID of the environment to retrieve
            project_id (int or list, optional): The project ID or IDs
            state (int, optional): 1 = active, 2 = deleted
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
            order_by (str, optional): Field to order the result by.
                Use - to indicate reverse order.
        """
        return self._simple_request(
            f"accounts/{account_id}/jobs/",
            params={
                "environment_id": environment_id,
                "project_id__in": json_listify(project_id),
                "state": state,
                "offset": offset,
                "limit": limit,
                "order_by": order_by,
            },
        )

    @v2
    def list_run_artifacts(
        self,
        account_id: int,
        run_id: int,
        *,
        step: int = None,
    ) -> Dict:
        """Fetch a list of artifact files generated for a completed run.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            run_id (int): Numeric ID of the run to retrieve
            step (str, optional): The index of the Step in the Run to query for
                artifacts. The first step in the run has the index 1. If the step
                parameter is omitted, then this endpoint will return the artifacts
                compiled for the last step in the run.
        """
        return self._simple_request(
            f"accounts/{account_id}/runs/{run_id}/artifacts",
            params={"step": step},
        )

    @v2
    def list_runs(
        self,
        account_id: int,
        *,
        include_related: List[str] = None,
        job_definition_id: int = None,
        environment_id: int = None,
        project_id: Union[int, List[int]] = None,
        deferring_run_id: int = None,
        status: Union[List[str], str] = None,
        order_by: str = None,
        offset: int = None,
        limit: int = None,
    ) -> Dict:
        """List runs in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            include_related (list): List of related
                fields to pull with the run. Valid values are `trigger`, `job`,
                `repository`, `debug_logs`, `run_steps`, and `environment`.
            job_definition_id (int, optional): Applies a filter to only return
                runs from the specified Job.
            environment_id (int, optional): Numeric ID of the environment
            project_id (int or list, optional): The project ID or IDs
            deferring_run_id (int, optional): Numeric ID of a deferred run
            status (str or list, optional): The status to apply when listing runs.
                Options include queued, starting, running, success, error, and
                cancelled
            order_by (str, optional): Field to order the result by.
                Use - to indicate reverse order.
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
        """
        if status is not None:
            try:
                status = [getattr(JobRunStatus, s.upper()) for s in listify(status)]
            except AttributeError:
                raise
            else:
                status = json.dumps(status)
        return self._simple_request(
            f"accounts/{account_id}/runs",
            params={
                "include_related": ",".join(include_related or []),
                "job_definition_id": job_definition_id,
                "environment_id": environment_id,
                "project_id__in": json_listify(project_id),
                "deferring_run_id": deferring_run_id,
                "order_by": order_by,
                "offset": offset,
                "limit": limit,
                "status__in": status,
            },
        )

    @v3
    def list_users(
        self,
        account_id: int,
        *,
        state: int = None,
        limit: int = None,
        offset: int = None,
        order_by: str = "email",
    ) -> Dict:
        """List users in an account.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            state (int, optional): 1 = active, 2 = deleted
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
            order_by (str, optional): Field to order the result by.
                Use - to indicate reverse order.
        """
        return self._simple_request(
            f"accounts/{account_id}/users/",
            params={
                "limit": limit,
                "offset": offset,
                "order_by": order_by,
                "state": state,
            },
        )

    @v3
    def list_webhooks(
        self,
        account_id: int,
        *,
        limit: int = None,
        offset: int = None,
    ) -> Dict:
        """List of webhooks in account
        Args:
            account_id (int): Numeric ID of the account
            limit (int, optional): The limit to apply when listing runs.
                Use with offset to paginate results.
            offset (int, optional): The offset to apply when listing runs.
                Use with limit to paginate results.
        """
        return self._simple_request(
            f"accounts/{account_id}/webhooks/subscriptions",
            params={"limit": limit, "offset": offset},
        )

    @v3
    def test_connection(self, account_id: int, payload: Dict) -> Dict:
        """Test a connection

        Args:
            account_id (int): Numeric ID of the account
            payload (dict): Dictionary representing the connection to test
        """
        return self._simple_request(
            f"accounts/{account_id}/connections/test/", method="post", json=payload
        )

    @v3
    def test_webhook(self, account_id: int, webhook_id: str) -> Dict:
        """Test a webhook

        Args:
            account_id (int): Numeric ID of the account
            webhook_id (str): String ID of the webhook you want to test
        """
        return self._simple_request(
            f"accounts/{account_id}/webhooks/subscription/{webhook_id}/test",
        )

    def _poll_for_completion(self, run: Dict, poll_interval: int = 10):
        start = time.time()
        run_id = run["data"]["id"]
        account_id = run["data"]["account_id"]
        while True:
            time.sleep(poll_interval)
            run = self.get_run(account_id, run_id)
            status = run["data"]["status"]
            self.console.log(self._run_status_formatted(run, time.time() - start))
            if status in [
                JobRunStatus.SUCCESS,
                JobRunStatus.CANCELLED,
                JobRunStatus.ERROR,
            ]:
                break
        return run

    def _run_status_formatted(self, run: Dict, time: float) -> str:
        """Format a string indicating status of job.
        Args:
            run (dict): Dictionary representation of a Run
            time (float): Elapsed time since job triggered
        """
        status = JobRunStatus(run["data"]["status"]).name
        url = run["data"]["href"]
        return (
            f'Status: "{status.capitalize()}"\nElapsed time: {round(time, 0)}s\n'
            f"View here: {url}"
        )

    @v2
    def trigger_autoscaling_ci_job(
        self,
        account_id: int,
        job_id: int,
        payload: Dict,
        *,
        should_poll: bool = False,
        poll_interval: int = 10,
        delete_cloned_job: bool = True,
        max_run_slots: int = None,
    ):
        """Trigger an autoscaling CI job

        !!! info

            In the event your CI job is already running, this will do the following:

            - If a new commit is created for the currently running job, cancel the
              job and then trigger again
            - If this is an entirely new pull request, clone the job and trigger
            - This will also check to see if your account has met or exceeded the
              allotted run slots.  In the event you have, a cloned job will
              not be created and the existing job will be triggered.

        More info [here](/latest/guide/autoscaling_ci)

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to trigger
            payload (dict): Payload required in triggering a job.  It's important that
                the payload consists of the following keys in order to mimic the
                native behavior of dbt Cloud's Slim CI functionality:

                - `git_sha`
                - `cause`
                - `schema_override`
                - Depending on your git provider, one of `github_pull_request_id`,
                  `gitlab_merge_request_id`, or `azure_pull_request_id`
            should_poll (bool, optional): Poll until completion if `True`, completion
                is one of success, failure, or cancelled
            poll_interval (int, optional): Number of seconds to wait in between
                polling
            delete_cloned_job (bool, optional): Indicate if cloned job should be
                deleted after being triggered
            max_run_slots (int, optional): Number of run slots that should be
                available to this process.  This will limit the ability to run
                concurrent PRs up the the allocated run slots for your account.  When
                set to `None`, the `run_slots` allocated to your account will be used
                to determine if a job should be cloned.
        """
        self.console.log("Finding any in progress runs...")
        cloned_job = None
        payload_pr_id = None
        pull_request_key: Optional[str] = None

        # Get all runs in "running" state
        in_progress_runs = self.list_runs(
            account_id,
            status=["queued", "starting", "running"],
            include_related=["trigger"],
        ).get("data", [])

        # Find any runs that match the job_id specified in function signature
        in_progress_job_run = [
            r for r in in_progress_runs if r.get("job_definition_id", -1) == job_id
        ]

        # Find the valid pull_request_key to use in pulling out relevant PR IDs
        for pull_request_key in PULL_REQUESTS:
            if pull_request_key in payload:
                payload_pr_id = payload[pull_request_key]
                break
        else:
            pull_request_key = None

        # This will be used to identify if the PR within the payload has a run
        # that's in a running state.
        in_progress_pr_run = [
            r
            for r in in_progress_runs
            if r.get("trigger", {}).get(pull_request_key, -1) == payload_pr_id
        ]

        if in_progress_pr_run:
            # A PR should only have one run in a queued, running, or starting state
            # at any given time
            pr_run = in_progress_pr_run[0]
            self.console.log(
                f"Found an in progress run for PR #{payload_pr_id}.  Run "
                f'{pr_run["id"]} will be canceled and a job triggered for the new '
                "commit."
            )
            _ = self.cancel_run(account_id, pr_run["id"])
        else:
            pr_run = {}

        if in_progress_job_run:
            # Job can only have one run in a queued, running, or starting state
            job_run = in_progress_job_run[0]
            job_run_is_pr_run = pr_run.get("id", None) == job_run["id"]

            # Only clone the job if this job run isn't the same as the PR run we just
            # cancelled above
            if not job_run_is_pr_run:
                run_slots = (
                    self.get_account(account_id).get("data", {}).get("run_slots", 0)
                )
                max_run_slots = min(max_run_slots or run_slots, run_slots)
                if max_run_slots > len(in_progress_runs):
                    self.console.log(
                        f'Job {job_id} is currently being used in run {job_run["id"]}. '
                        "This job definition will be cloned and then triggered for "
                        f"pull request #{payload_pr_id}."
                    )
                    current_job = self.get_job(account_id, job_id).get("data", {})

                    # Alter the current job definition so it can be cloned
                    read_only_fields = ["is_deferrable", "raw_dbt_version", "job_type"]
                    for read_only_field in read_only_fields:
                        current_job.pop(read_only_field)
                    current_job["id"] = None
                    now = datetime.now().strftime("%m/%d/%Y %H:%M:%S")
                    current_job["name"] = current_job["name"] + f" [CLONED {now}]"
                    cloned_job = self.create_job(account_id, current_job)["data"]

                    # Modify the should_poll argument - this needs to be `True`
                    # if we're deleting the cloned job.  Otherwise, dbt Cloud
                    # will cancel the run because it can't find an associated job
                    if delete_cloned_job:
                        should_poll = True
                    job_id = cloned_job["id"]
                else:
                    self.console.log(
                        "Not cloning the job as your account has met or exceeded the "
                        "number of run slots or a limit was placed by the user.  The "
                        "normal job will be queued."
                    )
        else:
            self.console.log("No in progress job run found.  Triggering as normal")
        run = self.trigger_job(
            account_id,
            job_id,
            payload,
            should_poll=should_poll,
            poll_interval=poll_interval,
        )

        if cloned_job is not None and delete_cloned_job:
            self.delete_job(account_id, job_id)
        return run

    @v2
    def trigger_job_from_failure(
        self,
        account_id: int,
        job_id: int,
        *,
        should_poll: bool = True,
        poll_interval: int = 10,
    ):
        """Trigger job from point of failure

        Use this method to retry a failed run for a job from the point of failure, if
        the run failed. Otherwise trigger a new run.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to trigger
        """
        run = self._simple_request(
            f"accounts/{account_id}/jobs/{job_id}/rerun/",
            method="post",
        )
        self.console.log(self._run_status_formatted(run, 0))
        if should_poll:
            run = self._poll_for_completion(run, poll_interval)

        return run

    @v2
    def trigger_job(
        self,
        account_id: int,
        job_id: int,
        payload: Dict,
        *,
        should_poll: bool = True,
        poll_interval: int = 10,
        retries: int = 0,
    ):
        """Trigger a job by its ID

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to trigger
            payload (dict): Payload required for post request
            should_poll (bool, optional): Poll until completion if `True`, completion
                is one of success, failure, or cancelled
            poll_interval (int, optional): Number of seconds to wait in between
                polling
            retries (int, optional): Number of times to retry a failed job
        """

        def is_run_complete(run: Dict):
            return run["data"]["status"] in [
                JobRunStatus.SUCCESS,
                JobRunStatus.CANCELLED,
            ]

        run = self._simple_request(
            f"accounts/{account_id}/jobs/{job_id}/run/",
            method="post",
            json=payload,
        )
        if not run["status"]["is_success"]:
            self.console.log(f"Run NOT triggered for job {job_id}.  See run response.")
            return run

        self.console.log(self._run_status_formatted(run, 0))
        if should_poll or retries > 0:
            run = self._poll_for_completion(run, poll_interval)
            while retries > 0 and not is_run_complete(run):
                self.console.log(
                    f"Retrying job {job_id} after failure.  Retries left: {retries - 1}"
                )
                run = self.trigger_job_from_failure(account_id, job_id)
                retries -= 1

        return run

    @v3
    def update_environment_variables(
        self, account_id: int, project_id: int, payload: Dict
    ):
        """Update an environment variable

        Args:
            account_id (int): Numeric ID of the account
            project_id (int): Numeric ID of the project
            payload (dict): Dictionary representing the environment to update
        """
        return self._simple_request(
            f"accounts/{account_id}/projects/{project_id}/environment-variables/bulk",  # noqa: E501
            method="put",
            json=payload,
        )

    @v2
    def update_job(self, account_id: int, job_id: int, payload: Dict) -> Dict:
        """Update a job by its ID.

        Args:
            account_id (int): Numeric ID of the account to retrieve
            job_id (int): Numeric ID of the job to retrieve
            payload (dict): Payload required for post request
        """
        return self._simple_request(
            f"accounts/{account_id}/jobs/{job_id}/",
            method="post",
            json=payload,
        )

    @v3
    def update_webhook(self, account_id: int, webhook_id: str, payload: Dict) -> Dict:
        """Update a webhook

        Args:
            account_id (int): Numeric ID of the account
            webhook_id (str): String ID of the webhook you want to update
            payload (dict): Dictionary representing the webhook to update
        """
        return self._simple_request(
            f"accounts/{account_id}/webhooks/subscription/{webhook_id}",
            method="put",
            json=payload,
        )
