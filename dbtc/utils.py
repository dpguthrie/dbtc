# stdlib
import json
from typing import Any

__all__ = ["listify", "json_listify"]


def listify(value: Any):
    if isinstance(value, list):
        return value[:]
    else:
        return [value]


def json_listify(value: Any):
    if value is not None:
        return json.dumps(listify(value))

    return value
