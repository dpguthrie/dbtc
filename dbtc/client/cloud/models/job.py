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


class Job(BaseModel):

    # Required
    account_id: int
    environment_id: int
    generate_docs: bool
    name: str
    project_id: int
    run_generate_sources: bool
    state: Literal[State.active, State.deleted]

    # Optional
    dbt_version: Optional[str] = None
    deactivated: bool = False
    deferring_job_definiton_id: Optional[int] = None
    execute_steps: Optional[List[str]] = None
    execution: Optional[_JobExecution] = None
    id: Optional[int] = None
    is_deferrable: Optional[bool] = False
    run_failure_count: int = 0
    schedule: Optional[_JobSchedule] = None
    settings: Optional[_JobSettings] = None
    triggers: Optional[_JobTrigger] = None

    def __init__(self, **data):
        schedule = data.get('schedule', {})
        date = schedule.get('date', {}).get('type', None)
        time = schedule.get('time', {}).get('type', None)
        if date is not None:
            data['schedule']['date'] = date
        if time is not None:
            data['schedule']['time'] = time
        super().__init__(**data)
