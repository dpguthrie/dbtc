# stdlib
from typing import Literal, Optional

# third party
from pydantic import BaseModel, conlist


class Webhook(BaseModel):

    # Required
    active: bool
    client_url: str
    event_types: conlist(  # type: ignore
        Literal['job.run.started', 'job.run.completed', 'job.run.errored'],
        unique_items=True,
    )
    name: str

    # Optional
    deactivate_reason: Optional[str]
    description: Optional[str]
    id: Optional[str]
    job_ids: Optional[conlist(int, unique_items=True)]  # type: ignore
