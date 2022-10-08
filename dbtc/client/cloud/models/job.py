# stdlib
from typing import Any, Dict, List, Literal, Optional

# third party
from pydantic import BaseModel


class _JobExecution(BaseModel):
    timeout_seconds: int


class _JobSchedule(BaseModel):
    cron: str
    date: Dict[str, Any]
    time: Dict[str, Any]


class _JobSettings(BaseModel):
    threads: int
    target_name: str


class _JobTrigger(BaseModel):
    custom_branch_only: Optional[bool]
    git_provider_webhook: Optional[bool]
    github_webhook: bool
    schedule: bool


class Job(BaseModel):

    # Required
    account_id: int
    dbt_version: str
    environment_id: int
    execution: _JobExecution
    generate_docs: bool
    name: str
    project_id: int
    run_generate_sources: bool
    schedule: _JobSchedule
    settings: _JobSettings
    triggers: _JobTrigger
    state: Literal[1, 2]

    # Optional
    deactivated: Optional[bool] = False
    deferring_job_definition_id: Optional[int]
    execute_steps: Optional[List[str]]
    id: Optional[int]
    lifecycle_webhooks: Optional[bool]
    lifecycle_webhooks_url: Optional[str]
    run_failure_count: Optional[int] = 0
