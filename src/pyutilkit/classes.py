from __future__ import annotations

import threading
from typing import TypeVar, cast

_T = TypeVar("_T")


class Singleton(type):
    instance: object
    _lock: threading.Lock

    def __init__(
        cls, name: str, bases: tuple[type[object], ...], namespace: dict[str, object]
    ) -> None:
        super().__init__(name, bases, namespace)
        cls.instance = None
        cls._lock = threading.Lock()

    def __call__(cls: type[_T]) -> _T:
        mcs = cast("Singleton", cls)
        if mcs.instance is None:
            with mcs._lock:
                if mcs.instance is None:
                    mcs.instance = super(Singleton, mcs).__call__()
        return cast("_T", mcs.instance)
