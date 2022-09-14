# This dictionary contains job_ids and what the associated
# override steps should be when restarting from failure.
JOB_ASSERTIONS = {
    121820: ['dbt build -s bad_model'],
    121821: ['dbt build -s unique_good_model_clerk_name'],
    121822: [
        'dbt build -s bad_model',
        'dbt run-operation bad_macro',
    ],
    121823: ['dbt run-operation bad_macro'],
    121824: [
        'dbt build -s bad_model',
        'dbt run-operation bad_macro',
    ],
    121825: ['dbt run -s bad_model'],
    121826: ['dbt test -s unique_good_model_clerk_name'],
    121830: ['dbt seed -s bad_seed'],
    121832: ['dbt snapshot -s bad_snapshot'],
    122458: ['dbt run -s bad_model --vars \'{"key": "value"}\''],
    122473: [
        'dbt build -s unique_good_model_clerk_name --vars \'{key: value, other_key: other_value}\'',  # noqa: E501
        'dbt run-operation good_macro --args \'{arg_1: value_1}\'',
    ],
    128120: [
        'dbt --use-experimental-parser run -s bad_model --vars \'{"key": "value"}\'',
    ],
    128138: [
        (
            'dbt build -s unique_order_items_bad_order_key '
            'fct_order_items_bad fct_orders_bad not_null_fct_orders_bad_order_key '
            'relationships_fct_orders_bad_customer_key__customer_key__ref_dim_customers_ '  # noqa: E501
            'unique_fct_orders_bad_order_key'
        ),
        'dbt run-operation good_macro',
        'dbt docs generate',
    ],
}

ACCOUNT_ID = 43786


def _test_job(dbtc_client, job_id: int):
    run_id = dbtc_client.cloud.trigger_job(
        ACCOUNT_ID,
        job_id,
        payload={'cause': 'Testing dbtc'},
        should_poll=False,
        restart_from_failure=True,
    )['data']['id']
    steps_override = dbtc_client.cloud.get_run(
        ACCOUNT_ID, run_id, include_related=['trigger']
    )['data']['trigger']['steps_override']
    assert steps_override == JOB_ASSERTIONS[job_id]


def test_restart_from_failure(dbtc_client):
    for job_id in JOB_ASSERTIONS.keys():
        _test_job(dbtc_client, job_id)
