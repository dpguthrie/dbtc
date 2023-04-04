# stdlib
from typing import List, Literal, Optional

# third party
from pydantic import BaseModel, validator


class _JobExecution(BaseModel):
    timeout_seconds: int

    @validator('timeout_seconds')
    def validate_timeout_seconds(cls, v):
        if not 0 <= v <= 86400:
            raise ValueError('Timeout seconds must be between 0 and 86400')
        return v


class _JobSchedule(BaseModel):
    cron: str
    date: Literal['custom_cron', 'days_of_week', 'every_day']
    time: Literal['every_hour', 'at_exact_hours']


class _JobSettings(BaseModel):
    threads: int
    target_name: str

    @validator('threads')
    def validate_threads(cls, v):
        if v < 1:
            raise ValueError('Threads must be greater than 0')
        return v


class _JobTrigger(BaseModel):
    github_webhook: bool
    schedule: bool
    custom_branch_only: Optional[bool]
    git_provider_webhook: Optional[bool]


class Job(BaseModel):

    # Required
    account_id: int
    environment_id: int
    generate_docs: bool
    name: str
    project_id: int
    run_generate_sources: bool
    state: Literal[1, 2]

    # Optional
    dbt_version: Optional[str]
    deactivated: Optional[bool]
    deferring_job_definiton_id: Optional[int]
    execute_steps: Optional[List[str]]
    execution: Optional[_JobExecution]
    id: Optional[int]
    is_deferrable: Optional[bool]
    schedule: Optional[_JobSchedule]
    settings: Optional[_JobSettings]
    triggers: Optional[_JobTrigger]
