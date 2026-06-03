from __future__ import annotations
import time
from typing import Any

_store: dict[str, tuple[Any, float]] = {}


def get(key: str, ttl: float) -> tuple[bool, Any]:
    entry = _store.get(key)
    if entry and time.monotonic() - entry[1] < ttl:
        return True, entry[0]
    return False, None


def set(key: str, value: Any) -> None:
    _store[key] = (value, time.monotonic())


def invalidate(*keys: str) -> None:
    for k in keys:
        _store.pop(k, None)


def invalidate_prefix(prefix: str) -> None:
    for k in list(_store.keys()):
        if k.startswith(prefix):
            _store.pop(k, None)
