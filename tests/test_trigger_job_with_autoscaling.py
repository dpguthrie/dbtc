import time

# This dictionary contains job_ids and what the associated
# override steps should be when restarting from failure.
JOB_ASSERTIONS = {
    133168: {'execute_steps': ['dbt build  -s state:modified+']},
}

ACCOUNT_ID = 28885

def _test_job(dbtc_client, job_id: int):
    
    first_run = dbtc_client.cloud.trigger_job(
        ACCOUNT_ID,
        job_id,
        payload={'cause': 'Testing dbtc'},
        should_poll=False,
    )['data']
    
    # wait a few seconds to make sure the first job's status has been updated
    time.sleep(3)
    second_run = dbtc_client.cloud.trigger_job_with_autoscaling(
        ACCOUNT_ID,
        job_id,
        payload={'cause': 'Testing dbtc'},
        autoscale_delete_post_run=True,
    )['data']

    # check that we triggered distinct jobs
    assert first_run['job_definition_id'] != second_run['job_definition_id']
    
    # get the first and second runs with run steps included
    first_run_data = dbtc_client.cloud.get_run(
        account_id=ACCOUNT_ID,
        run_id=first_run['id'],
        include_related=['run_steps']
    )['data']
    
    second_run_data = dbtc_client.cloud.get_run(
        account_id=ACCOUNT_ID,
        run_id=second_run['id'],
        include_related=['run_steps']
    )['data'] 
    # check that the run steps are the same for the original and replicated jobs
    first_run_step_names = [step['name'] for step in first_run_data['run_steps']]
    second_run_step_names = [step['name'] for step in second_run_data['run_steps']]

    assert first_run_step_names == second_run_step_names 


def test_trigger_job_with_autoscaling(dbtc_client):
    for job_id in JOB_ASSERTIONS.keys():
        _test_job(dbtc_client, job_id)
