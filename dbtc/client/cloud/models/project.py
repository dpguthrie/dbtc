# stdlib
from typing import Optional

# third party
from pydantic import BaseModel

from .constants import State


class Project(BaseModel):

    # Required
    account_id: int
    name: str

    # Optional
    id: Optional[int] = None
    connection_id: Optional[int] = None
    dbt_project_subdirectory: Optional[str] = None
    docs_job_id: Optional[int] = None
    freshness_job_id: Optional[int] = None
    repository_id: Optional[int] = None
    state: int = State.active
