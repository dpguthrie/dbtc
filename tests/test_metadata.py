JOB_ID = 73796
ENVIRONMENT_ID = 218762
QUERY = """
query Environment($environmentId: BigInt!, $first: Int!, $after: String) {
    environment(id: $environmentId) {
        applied {
            models(first: $first, after: $after) {
                pageInfo {
                    startCursor
                    endCursor
                    hasNextPage
                }
                edges {
                    node {
                        uniqueId
                        executionInfo {
                            lastSuccessJobDefinitionId
                            lastSuccessRunId
                            executionTime
                        }
                    }
                }
            }
        }
    }
}
"""


def test_query_no_variables(dbtc_client):
    query = f"{{models(jobId: {JOB_ID}) {{uniqueId}}}}"
    data = dbtc_client.metadata.query(query)
    assert "data" in data
    assert "error" not in data


def test_query_with_variables(dbtc_client):
    query = "query GetMetadata($jobId: Int!) {models(jobId: $jobId) {uniqueId}}"
    variables = {"jobId": JOB_ID}
    data = dbtc_client.metadata.query(query, variables)
    assert "data" in data
    assert "error" not in data


def test_pagination(dbtc_client):
    variables = {"environmentId": ENVIRONMENT_ID, "first": 25, "after": None}
    data = dbtc_client.metadata.query(QUERY, variables)
    assert isinstance(data[0], dict)
    assert "node" in data[0]


def test_pagination_without_combining_lists(dbtc_client):
    variables = {"environmentId": ENVIRONMENT_ID, "first": 25, "after": None}
    data = dbtc_client.metadata.query(QUERY, variables, paginated_request_to_list=False)
    print(data)
    assert isinstance(data[0], dict)
    assert "data" in data[0]


def test_pagination_with_max_pages(dbtc_client):
    variables = {"environmentId": ENVIRONMENT_ID, "first": 25, "after": None}
    data = dbtc_client.metadata.query(QUERY, variables, max_pages=1)
    assert isinstance(data[0], dict)
    assert len(data) == 25
