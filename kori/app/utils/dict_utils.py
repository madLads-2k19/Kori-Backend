from typing import Any


def remove_null_values(dictionary: dict[Any, Any]) -> dict[Any, Any]:
    return dict([(k, v) for k, v in dictionary.items() if v is not None])
