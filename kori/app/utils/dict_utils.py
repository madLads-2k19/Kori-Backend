from typing import Any


def remove_null_values(dictionary: dict[Any, Any]) -> dict[Any, Any]:
    return {k: v for k, v in dictionary.items() if v is not None}
