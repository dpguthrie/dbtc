# stdlib
from typing import List, Literal, Optional

# third party
from pydantic import BaseModel

from .constants import State


class _JobExecution(BaseModel):
    timeout_seconds: int


class _JobSchedule(BaseModel):
    cron: str
    date: Literal['custom_cron', 'days_of_week', 'every_day']
    time: Literal['every_hour', 'at_exact_hours']


class _JobSettings(BaseModel):
    threads: int
    target_name: str


class _JobTrigger(BaseModel):
    github_webhook: bool
    schedule: bool
    git_provider_webhook: Optional[bool] = None


class Test(BaseModel):
    account_id: int
    id: Optional[int] = None

class Job(BaseModel):

    # Required
    account_id: int
    environment_id: int
    generate_docs: bool
    name: str
    dbt_version: str
    project_id: int
    run_generate_sources: bool
    schedule: _JobSchedule
    settings: _JobSettings
    triggers: _JobTrigger
    state: Literal[State.active, State.deleted]

    # Optional
    deactivated: Optional[bool] = False
    deferring_job_definition_id: Optional[int] = None
    execute_steps: Optional[List[str]] = None
    execution: Optional[_JobExecution] = None
    is_deferrable: Optional[bool] = False
    run_failure_count: int = 0

    def __init__(self, **data):
        schedule = data.get('schedule', {})
        date = schedule.get('date', {}).get('type', None)
        time = schedule.get('time', {}).get('type', None)
        if date is not None:
            data['schedule']['date'] = date
        if time is not None:
            data['schedule']['time'] = time
        super().__init__(**data)
