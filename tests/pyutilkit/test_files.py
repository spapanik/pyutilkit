import os
from pathlib import Path

import pytest

from pyutilkit.files import handle_exceptions, hash_file


def test_handle_exceptions_handled_exception() -> None:
    @handle_exceptions(exceptions=(ZeroDivisionError,), default=0.0)
    def invert(n: int) -> float:
        return 1 / n

    assert invert(1) == 1
    assert invert(0) == 0


def test_handle_exceptions_unhandled_exception() -> None:
    @handle_exceptions(exceptions=(TypeError,), default=0.0)
    def invert(n: int) -> float:
        return 1 / n

    assert invert(1) == 1
    pytest.raises(ZeroDivisionError, invert, 0)


def test_hash_file() -> None:
    dev_null_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert hash_file(Path(os.devnull)) == dev_null_hash
