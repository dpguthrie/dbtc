# stdlib
from typing import Literal, Optional

# third party
from pydantic import BaseModel, conlist


class Webhook(BaseModel):
    # Required
    active: bool
    client_url: str
    event_types: conlist(  # type: ignore
        Literal["job.run.started", "job.run.completed", "job.run.errored"],
    )
    name: str

    # Optional
    deactivate_reason: Optional[str] = None
    description: Optional[str] = None
    id: Optional[str] = None
    job_ids: Optional[int] = None
