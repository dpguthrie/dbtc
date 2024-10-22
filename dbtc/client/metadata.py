# stdlib
from typing import Any, Dict, List, Union

# first party
from dbtc.client.base import _Client

QUERIES = {
    "column_lineage": """
query ColumnLineage($environmentId: BigInt!, $nodeUniqueId: String!, $filters: ColumnLineageFilter) {
  column(environmentId: $environmentId) {
    lineage(nodeUniqueId: $nodeUniqueId, filters: $filters) {
      accountId
      projectId
      environmentId
      runId
      nodeUniqueId
      uniqueId
      name
      parentColumns
      childColumns
      relationship
      isError
      error
      errorCategory
    }
  }
}
    """,  # noqa: E501
    "mesh_projects": """
query MeshProjects($accountId: BigInt!) {
  account(id: $accountId) {
    meshProjects {
      dbtCoreProject
      dbtCloudProject
      projectId
      defaultEnvironmentId
      isProducer
      isConsumer
      projectSummary {
        totalNodes
        totalModels
        publicModels
        sources
        metrics
        semanticModels
        tests
        snapshots
        exposures
        macros
        seeds
      }
      dependentProjects {
        dbtCoreProject
        dbtCloudProject
        projectId
        defaultEnvironmentId
        isProducer
        isConsumer
      }
    }
  }
}
    """,
    "model_execution_history": """
query Performance($environmentId: BigInt!, $startDate: Date!, $endDate: Date!, $uniqueId: String!) {
  performance(environmentId: $environmentId) {
    modelExecutionHistory(startDate: $startDate, endDate: $endDate, uniqueId: $uniqueId) {
      date
      meanExecutionTime
      executionTimes
      executionsByJob {
        jobId
        meanExecutionTime
        executionTimes
        executions {
          runId
          runStartedAt
          executionTime
          status
          isFullRefresh
          executionStartedAt
          adapter
          queryId
        }
      }
    }
  }
}
    """,  # noqa: E501
    "most_executed_models": """
query Performance($environmentId: BigInt!, $start: Date!, $end: Date!, $limit: Int, $jobLimit: Int) {
  performance(environmentId: $environmentId) {
    mostExecutedModels(start: $start, end: $end, limit: $limit, jobLimit: $jobLimit) {
      uniqueId
      totalExecutions
      byJob {
        jobId
        totalExecutions
      }
    }
  }
}
    """,  # noqa: E501
    "longest_executed_models": """
query Performance($environmentId: BigInt!, $start: Date!, $end: Date!, $limit: Int, $jobId: BigInt, $orderBy: SortAggregation, $jobLimit: Int) {
  performance(environmentId: $environmentId) {
    longestExecutedModels(start: $start, end: $end, limit: $limit, jobId: $jobId, orderBy: $orderBy, jobLimit: $jobLimit) {
      uniqueId
      maxExecutionTime
      averageExecutionTime
      byJob {
        jobId
        maxExecutionTime
        averageExecutionTime
      }
    }
  }
}
    """,  # noqa: E501
    "most_execution_failed_models": """
query Performance($environmentId: BigInt!, $start: Date!, $end: Date!, $limit: Int) {
  performance(environmentId: $environmentId) {
    mostExecutionFailedModels(start: $start, end: $end, limit: $limit) {
      uniqueId
      failurePercentage
      totalExecutions
      totalFailedExecutions
    }
  }
}
    """,
    "most_test_failed_models": """
query Performance($environmentId: BigInt!, $start: Date!, $end: Date!, $limit: Int) {
  performance(environmentId: $environmentId) {
    mostTestFailedModels(start: $start, end: $end, limit: $limit) {
      uniqueId
      failurePercentage
      totalRunsWithTests
      totalRunsWithTestFailures
    }
  }
}
    """,
    "model_job_information": """
query Performance($environmentId: BigInt!, $start: Date!, $end: Date!, $uniqueId: String!) {
  performance(environmentId: $environmentId) {
    jobInformation(start: $start, end: $end, uniqueId: $uniqueId) {
      jobId
      name
    }
  }
}
    """,  # noqa: E501
    "recommendations": """
query Recommendations($environmentId: BigInt!, $first: Int!, $after: String, $filter: RuleFilter) {
  recommendations(environmentId: $environmentId) {
    metrics {
      name
      value
    }
    rules(first: $first, after: $after, filter: $filter) {
      edges {
        node {
          name
          category
          severity
          uniqueId
          violationId
          description
        }
      }
      pageInfo {
        startCursor
        endCursor
        hasNextPage
      }
      totalCount
    }
  }
}
    """,  # noqa: E501
    "public_models": """
query Node($accountId: BigInt!, $after: String, $filter: PublicModelsFilter, $first: Int) {
  account(id: $accountId) {
    publicModels(after: $after, filter: $filter, first: $first) {
      edges {
        node {
          accountId
          columnCount
          database
          dbtCoreProject
          dependentProjects {
            dbtCoreProject
            defaultEnvironmentId
            dependentModelsCount
            environmentId
            projectId
          }
          deprecationDate
          description
          environmentDeploymentType
          environmentId
          fqn
          group
          healthIssues
          identifier
          isDefaultEnv
          lastRunStatus
          latestVersion
          materializationType
          name
          packageName
          projectId
          publicAncestors {
            accountId
            database
            dbtCoreProject
            description
            environmentDeploymentType
            environmentId
            fqn
            group
            healthIssues
            identifier
            isDefaultEnv
            lastRunStatus
            latestVersion
            materializationType
            name
            packageName
            projectId
            relationName
            runGeneratedAt
            schema
            uniqueId
          }
          relationName
          runGeneratedAt
          schema
          uniqueId
        }
      }
    }
  }
}
    """,
    "search": """
query Search($filter: SearchQueryFilter!, $environmentId: BigInt!, $after: String, $first: Int) {
  environment(id: $environmentId) {
    applied {
      searchResults(filter: $filter, after: $after, first: $first) {
        edges {
          cursor
          node {
            highlight
            hit {
              accountId
              description
              environmentId
              filePath
              meta
              name
              projectId
              resourceType
              tags
              uniqueId
            }
            matchedField
          }
        }
      }
    }
  }
}
    """,  # noqa: E501
}

ACCESS_LEVELS = ["private", "protected", "public"]
SEARCH_FIELD_TYPES = ["code", "column", "description", "name", "relation"]
RESOURCE_TYPES = [
    "Exposure",
    "Macro",
    "Metric",
    "Model",
    "Seed",
    "SemanticModel",
    "Snapshot",
    "Source",
    "Test",
]


class _MetadataClient(_Client):
    def __init__(self, session, **kwargs):
        super().__init__(session, **kwargs)

    _header_property = "service_token"

    @property
    def _path(self):
        if self._use_beta:
            return "/beta/graphql"

        return "/graphql"

    @property
    def _base_url(self):
        return f"https://metadata.{self._host}{self._path}"

    def _find_page_info(self, response_data: Dict):
        for key, value in response_data.items():
            if key == "pageInfo":
                return value

            if isinstance(value, dict):
                result = self._find_page_info(value)
                if result is not None:
                    return result

        return None

    def _find_list_element(self, response_data: Dict):
        for _, value in response_data.items():
            if isinstance(value, list):
                return value

            elif isinstance(value, dict):
                result = self._find_list_element(value)
                if result is not None:
                    return result

        return None

    def _make_request(self, payload: Dict[str, Any], after_cursor: str = None):
        if after_cursor:
            if "variables" not in payload:
                payload["variables"] = {}
            payload["variables"]["after"] = after_cursor

        response = self.session.post(self.full_url(), json=payload)
        return response.json()

    def _get_next_page_cursor(self, response: Dict) -> Union[str, None]:
        page_info = self._find_page_info(response)
        if page_info is None:
            return None

        if page_info.get("hasNextPage", False):
            return page_info["endCursor"]

        return None

    def column_lineage(
        self,
        environment_id: int,
        node_unique_id: str,
        *,
        max_depth: int = None,
        column_name: str = None,
        is_error: bool = False,
    ):
        """Retrieve column lineage for a given node.

        Args:
            environment_id (int): The environment id.
            node_unique_id (str): The unique id of the node.
            max_depth: (int): The max depth to traverse the lineage. Defaults to None.
            column_name: (str): The column name to filter by. Defaults to None.
            is_error: (bool): Whether to return only error nodes. Defaults to False.
        """
        variables = {
            "environmentId": environment_id,
            "nodeUniqueId": node_unique_id,
            "filters": {
                "maxDepth": max_depth,
                "columnName": column_name,
                "isError": is_error,
            },
        }
        return self.query(QUERIES["column_lineage"], variables=variables)

    def longest_executed_models(
        self,
        environment_id: int,
        start_date: str,
        end_date: str,
        *,
        limit: int = 5,
        job_limit: int = 5,
        job_id: int = None,
        order_by: str = "MAX",
    ):
        """Retrieve the longest executed models for a given environment.

        Args:
            environment_id (int): The environment id.
            start_date (str): The start date in the format YYYY-MM-DD.
            end_date (str): The end date in the format YYYY-MM-DD.
            limit (int, optional): The max number of models to return. Defaults to 5.
            job_limit (int, optional): The max number of jobs to return for each model.
                Defaults to 5.
            job_id (int, optional): The job id to filter by. Defaults to None.
            order_by (str, optional): The order by clause. One of "AVG" or "MAX".
                Defaults to "MAX".
        """
        if order_by not in ["AVG", "MAX"]:
            raise ValueError("order_by must be one of 'AVG' or 'MAX'")

        variables = {
            "environmentId": environment_id,
            "start": start_date,
            "end": end_date,
            "limit": limit,
            "jobLimit": job_limit,
            "jobId": job_id,
            "orderBy": order_by,
        }
        return self.query(QUERIES["longest_executed_models"], variables=variables)

    def mesh_projects(self, account_id: int):
        """Retrieve mesh projects for a given account.

        Args:
            account_id (int): The account id.
        """
        variables = {"accountId": account_id}
        return self.query(QUERIES["mesh_projects"], variables=variables)

    def model_execution_history(
        self, environment_id: int, start_date: str, end_date: str, unique_id: str
    ):
        """Retrieve model execution history for a given environment.

        Args:
            environment_id (int): The environment id.
            start_date (str): The start date in the format YYYY-MM-DD.
            end_date (str): The end date in the format YYYY-MM-DD.
            unique_id (str): The unique id of the model.
        """
        variables = {
            "environmentId": environment_id,
            "startDate": start_date,
            "endDate": end_date,
            "uniqueId": unique_id,
        }
        return self.query(QUERIES["model_execution_history"], variables=variables)

    def model_job_information(
        self, environment_id: int, start_date: str, end_date: str, unique_id: str
    ):
        """Retrieve model job information for a given environment.

        Args:
            environment_id (int): The environment id.
            start_date (str): The start date in the format YYYY-MM-DD.
            end_date (str): The end date in the format YYYY-MM-DD.
            unique_id (str): The unique id of the model.
        """
        variables = {
            "environmentId": environment_id,
            "start": start_date,
            "end": end_date,
            "uniqueId": unique_id,
        }
        return self.query(QUERIES["model_job_information"], variables=variables)

    def most_executed_models(
        self,
        environment_id: int,
        start_date: str,
        end_date: str,
        *,
        limit: int = 5,
        job_limit: int = 5,
    ):
        """Retrieve the most executed models for a given environment.

        Args:
            environment_id (int): The environment id.
            start_date (str): The start date in the format YYYY-MM-DD.
            end_date (str): The end date in the format YYYY-MM-DD.
            limit (int, optional): The max number of models to return. Defaults to 5.
            job_limit (int, optional): The max number of jobs to return for each model.
                Defaults to 5.
        """
        variables = {
            "environmentId": environment_id,
            "start": start_date,
            "end": end_date,
            "limit": limit,
            "jobLimit": job_limit,
        }
        return self.query(QUERIES["most_executed_models"], variables=variables)

    def most_failed_models(
        self, environment_id: int, start_date: str, end_date: str, *, limit: int = 5
    ):
        """Retrieve the most failed models for a given environment.

        Args:
            environment_id (int): The environment id.
            start_date (str): The start date in the format YYYY-MM-DD.
            end_date (str): The end date in the format YYYY-MM-DD.
            limit (int, optional): The max number of models to return. Defaults to 5.
        """
        variables = {
            "environmentId": environment_id,
            "start": start_date,
            "end": end_date,
            "limit": limit,
        }
        return self.query(QUERIES["most_execution_failed_models"], variables=variables)

    def most_models_test_failures(
        self, environment_id: int, start_date: str, end_date: str, *, limit: int = 5
    ):
        """Retrieve the most models with test failures for a given environment.

        Args:
            environment_id (int): The environment id.
            start_date (str): The start date in the format YYYY-MM-DD.
            end_date (str): The end date in the format YYYY-MM-DD.
            limit (int, optional): The max number of models to return. Defaults to 5.
        """
        variables = {
            "environmentId": environment_id,
            "start": start_date,
            "end": end_date,
            "limit": limit,
        }
        return self.query(QUERIES["most_test_failed_models"], variables=variables)

    def public_models(
        self,
        account_id: int,
        *,
        project_name: str = None,
        environment_ids: List[int] = None,
        project_id: int = None,
        unique_ids: List[str] = None,
    ):
        """Retrieve public models for a given account.

        Args:
            account_id (int): The account id.
            project_name (str, optional): The project name. Defaults to None.
            environment_ids (list[int], optional): The environment ids.
                Defaults to None.
            project_id (int, optional): The project id. Defaults to None.
            unique_ids (list[str], optional): The unique ids. Defaults to None.
        """
        variables = {
            "accountId": account_id,
            "filter": {
                "dbtCoreProjectName": project_name,
                "environmentIds": environment_ids,
                "projectId": project_id,
                "uniqueIds": unique_ids,
            },
        }
        return self.query(QUERIES["public_models"], variables=variables)

    def query(
        self,
        query: str,
        variables: Dict = None,
        max_pages: int = None,
        paginated_request_to_list: bool = False,
    ) -> Union[List[Dict], Dict]:
        """Query the Discovery API

        Args:
            query (str): The GraphQL query to execute.
            variables (Dict, optional): Dictionary containing the variables to include
                in the payload of the request.  Defaults to None.
            max_pages (int, optional): The max number of pages to paginate through when
                Defaults to None.
            paginated_request_to_list (bool, optional): When paginating through a
                request, the elements of the list within each request will be
                combined into a single list of dictionaries. Defaults to False.

        Returns:
            Union[List[Dict], Dict]: _description_
        """
        payload: Dict[str, Any] = {"query": query}
        if variables:
            payload.update({"variables": variables})
            if "first" in payload["variables"] and payload["variables"]["first"] > 500:
                raise ValueError("The maximum page size is 500.")

        # If we're not paginating, just make the request and return the results
        if "pageInfo" not in query:
            return self._make_request(payload)

        # If we're paginating but the query isn't setup properly for paginating,
        # then make a single request
        if query.count("$after") < 2:
            self.console.log(
                'Query not properly set up with an "$after" variable to paginate '
                "results properly so making a single request."
            )
            return self._make_request(payload)

        cursor = None
        all_results = []
        page = 0

        while True:
            response = self._make_request(payload, cursor)
            cursor = self._get_next_page_cursor(response)
            paginated_results = (
                self._find_list_element(response)
                if paginated_request_to_list
                else response
            )

            all_results.extend(
                paginated_results
            ) if paginated_request_to_list else all_results.append(paginated_results)
            page += 1

            if not cursor:
                break

            if max_pages and page >= max_pages:
                self.console.log(f"Reached max page limit of {max_pages}.")
                break

            self.console.log(f"Fetching page {page} for query...")

        return all_results

    def recommendations(
        self,
        environment_id: int,
        *,
        first: int = 500,
        severity: List[str] = None,
        categories: List[str] = None,
        rule_names: List[str] = None,
        unique_ids: List[str] = None,
    ):
        """Retrieve recommendations for a given environment.


        Args:
            environment_id (int): The environment id.
            first (int, optional): The max number of recommendations to return.
                Defaults to 10.
            severity (List[str], optional): The severity levels to filter by.
                Defaults to None.
            categories (List[str], optional): The categories to filter by.
                Defaults to None.
            rule_names (List[str], optional): The rule names to filter by.
                Defaults to None.
            unique_ids (List[str], optional): The unique ids to filter by.
                Defaults to None.
        """
        variables = {
            "environmentId": environment_id,
            "first": first,
            "filter": {
                "severity": severity,
                "categories": categories,
                "ruleNames": rule_names,
                "uniqueIds": unique_ids,
            },
        }
        return self.query(QUERIES["recommendations"], variables=variables)

    def search(
        self,
        environment_id: int,
        search_query: str,
        *,
        gql_query: str = None,
        first: int = 500,
        access_level: str = None,
        search_fields: List[str] = SEARCH_FIELD_TYPES,
        materialization_type: str = None,
        modeling_layer: str = None,
        resource_type: str = None,
        tags: str = None,
    ):
        """
        Search for resources in the metadata service.

        Args:
            environment_id (int): The environment id.
            search_query (str): The search query to filter by.
            gql_query (str, optional): Override the default GraphQL query with your own.
                Defaults to None and will use the default given by the package.
            first (int, optional): The max number of search results to return.
                Defaults to 500.
            access_levels (str, optional): The access levels to filter by.
                Defaults to None.
            search_fields (List[str], optional): The fields to search by. Defaults to
                ["code", "column", "description", "name", "relation"].
            materialization_type (str, optional): The materialization type to filter by.
                Defaults to None.
            modeling_layer (str, optional): The modeling layer to filter by.
                Defaults to None.
            resource_type (str, optional): The resource type to filter by.
                Defaults to None.
            tags (str, optional): The tags to filter by.
                Defaults to None.
        """
        query = gql_query or QUERIES["search"]
        if access_level and access_level not in ACCESS_LEVELS:
            raise ValueError(f"access_level must be one of {ACCESS_LEVELS}")

        if resource_type and resource_type not in RESOURCE_TYPES:
            raise ValueError(f"resource_type must be one of {RESOURCE_TYPES}")

        if any([f not in SEARCH_FIELD_TYPES for f in search_fields]):
            raise ValueError(
                f"search_fields must be one of {', '.join(SEARCH_FIELD_TYPES)}"
            )

        variables = {
            "filter": {
                "query": search_query,
                "accessLevels": access_level,
                "fields": search_fields,
                "materializationTypes": materialization_type,
                "modelingLayers": modeling_layer,
                "resourceTypes": resource_type,
                "tags": tags,
            },
            "environmentId": environment_id,
            "first": first,
        }
        return self.query(query, variables=variables)
