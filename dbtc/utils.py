# stdlib
import json
from typing import Any, List, Union


def listify(value: Any):
    if isinstance(value, list):
        return value[:]
    else:
        return [value]
