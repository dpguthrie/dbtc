# stdlib
from typing import Any


def listify(value: Any):
    if isinstance(value, list):
        return value[:]
    else:
        return [value]
