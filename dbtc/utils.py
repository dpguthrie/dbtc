# stdlib
import json
import re
from typing import Any

__all__ = ['listify', 'json_listify', 'camel_to_snake']


def listify(value: Any):
    if isinstance(value, list):
        return value[:]
    else:
        return [value]


def json_listify(value: Any):
    if value is not None:
        return json.dumps(listify(value))

    return value


def camel_to_snake(str):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', str).lower()
