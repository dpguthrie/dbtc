JOB_ID = 73796
IDENTIFIERS = {
    'exposure': 'sales_by_region',
    'macro': 'macro.tpch.money',
    'model': 'model.tpch.dim_customers',
    'seed': 'seed.tpch.country_codes',
    'test': 'test.tpch.unique_fct_order_items_order_item_key',
    'source': 'source.tpch.tpch.customer',
    'snapshot': 'snapshot.tpch.tpch_customer_snapshot',
}

COMMON_FIELDS = [
    'run_id',
    'account_id',
    'project_id',
    'environment_id',
    'job_id',
    'unique_id',
    'name',
]
SPECIFIC_FIELDS = {
    'exposure': ['parentsSources.name'],
    'metric': ['parents_models.columns.name'],
    'model': ['parents_sources.criteria.error_after.period'],
    'source': ['criteria.warnAfter.count'],
    'snapshot': ['parentsModels.unique_id'],
}


def test_methods_with_fields(dbtc_client):
    for resource, identifier in IDENTIFIERS.items():
        fields = COMMON_FIELDS + SPECIFIC_FIELDS.get(resource, [])
        method = f'get_{resource}'
        data = getattr(dbtc_client.metadata, method)(JOB_ID, identifier, fields=fields)
        assert 'data' in data
        method += 's'
        data = getattr(dbtc_client.metadata, method)(JOB_ID, fields=fields)
        assert 'data' in data


def test_methods_no_fields(dbtc_client):
    for resource, identifier in IDENTIFIERS.items():
        method = f'get_{resource}'
        data = getattr(dbtc_client.metadata, method)(JOB_ID, identifier)
        assert 'data' in data
        method += 's'
        data = getattr(dbtc_client.metadata, method)(JOB_ID)
        assert 'data' in data


def test_query_no_variables(dbtc_client):
    query = f'{{models(jobId: {JOB_ID}) {{uniqueId}}}}'
    data = dbtc_client.metadata.query(query)
    assert 'data' in data


def test_query_with_variables(dbtc_client):
    query = 'query GetMetadata($jobId: Int!) {models(jobId: $jobId) {uniqueId}}'
    variables = {'jobId': JOB_ID}
    data = dbtc_client.metadata.query(query, variables)
    assert 'data' in data
