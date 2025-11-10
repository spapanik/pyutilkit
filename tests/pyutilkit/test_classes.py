from __future__ import annotations

import threading
from time import sleep

from pyutilkit.classes import Singleton


def test_singleton() -> None:
    class MySingleton(metaclass=Singleton):
        pass

    assert MySingleton() is MySingleton()


def test_singleton_thread_safe() -> None:
    class MySingleton(metaclass=Singleton):
        def __init__(self) -> None:
            sleep(0.1)

    threads = []
    instances = []

    for _ in range(5):
        t = threading.Thread(target=lambda: instances.append(MySingleton()))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    singleton = MySingleton()
    assert all(instance is singleton for instance in instances)
