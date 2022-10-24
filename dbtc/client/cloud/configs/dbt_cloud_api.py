# stdlib
from typing import Dict


class dbtCloudAPIRequestFactory(object):
    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)

    def _create_job_request(self) -> Dict:
        """Minimal set of required fields needed to create a new dbt Cloud job,
        including default values
        """
        return {
            'name': None,
            'id': None,
            'execution': None,
            'account_id': None,
            'project_id': None,
            'environment_id': None,
            'dbt_version': None,
            'execute_steps': None,
            'state': None,
            'deferring_job_definition_id': None,
            'triggers': None,
            'settings': None,
            'schedule': None,
        }

    def create_job_request(self, data={}) -> Dict:
        """Completes the _create_job_request template with values from data and
           overrides

        Args:
          data (dict): payload to create the initial request. Typically, this will be
            the result of a GET on the job definition from an existing job to be used
            for dbt Cloud migrations
        """
        # copy everything EXCEPT for the existing dbt Cloud job ID
        result = self._create_job_request()
        if data != {}:
            for key in result.keys():
                if key != 'id':
                    result[key] = data[key]

        return result
