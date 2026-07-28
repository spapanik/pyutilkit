import hashlib
import logging
import os
from pathlib import Path
from typing import NoReturn, cast

import pytest

from pyutilkit.files import LogLevel, handle_exceptions, hash_file


def test_handle_exceptions_handled_exception() -> None:
    @handle_exceptions(exceptions=(ZeroDivisionError,), default=0.0)  # ty: ignore[invalid-argument-type]
    def invert(n: int) -> float:
        return 1 / n

    assert invert(1) == 1
    assert invert(0) == 0


def test_handle_exceptions_unhandled_exception() -> None:
    @handle_exceptions(exceptions=(TypeError,), default=0.0)  # ty: ignore[invalid-argument-type]
    def invert(n: int) -> float:
        return 1 / n

    assert invert(1) == 1
    with pytest.raises(ZeroDivisionError):
        invert(0)


def test_handle_exceptions_rejects_invalid_log_level_at_decoration_time() -> None:
    invalid_level = cast("LogLevel", "warnign")

    with pytest.raises(ValueError, match="Unsupported log level 'warnign'"):

        @handle_exceptions(log_level=invalid_level)
        def decorated() -> NoReturn:
            msg = "The wrapped function must not run"
            raise AssertionError(msg)


def test_handle_exceptions_logs_at_requested_level(
    caplog: pytest.LogCaptureFixture,
) -> None:
    fallback: str = "fallback"

    @handle_exceptions(  # ty: ignore[invalid-argument-type]
        exceptions=(RuntimeError,),
        default=fallback,
        log_level="error",
    )
    def fail() -> str:
        msg = "expected failure"
        raise RuntimeError(msg)

    with caplog.at_level(logging.ERROR, logger="pyutilkit.files"):
        result = fail()

    assert result == "fallback"
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelno == logging.ERROR
    assert record.exc_info is not None
    assert record.exc_info[0] is RuntimeError
    assert record.message.startswith("Function `fail` threw `RuntimeError`")


def test_handle_exceptions_logs_arguments_by_default(
    caplog: pytest.LogCaptureFixture,
) -> None:
    @handle_exceptions(exceptions=(ValueError,))
    def authenticate(user: str, *, api_key: str) -> None:
        if user and api_key:
            raise ValueError

    with caplog.at_level(logging.INFO, logger="pyutilkit.files"):
        authenticate("alice", api_key="secret")

    assert "args=('alice',)" in caplog.text
    assert "kwargs={'api_key': 'secret'}" in caplog.text


def test_handle_exceptions_can_suppress_arguments(
    caplog: pytest.LogCaptureFixture,
) -> None:
    @handle_exceptions(exceptions=(ValueError,), log_args=False)
    def authenticate(user: str, *, api_key: str) -> None:
        if user and api_key:
            raise ValueError

    with caplog.at_level(logging.INFO, logger="pyutilkit.files"):
        authenticate("alice", api_key="secret")

    record = caplog.records[0]
    assert record.message == "Function `authenticate` threw `ValueError`"
    assert record.exc_info is not None
    assert "alice" not in caplog.text
    assert "secret" not in caplog.text


def test_hash_file() -> None:
    dev_null_hash = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
    assert hash_file(Path(os.devnull)) == dev_null_hash


def test_hash_file_with_update(tmp_path: Path) -> None:
    tmp_file = tmp_path.joinpath("hello.txt")
    tmp_file.write_bytes(b"Hello, World!")
    hello_world_hash = (
        "dffd6021bb2bd5b0af676290809ec3a53191dd81c7f70a4b28688a362182986f"
    )
    assert hash_file(tmp_file, buffer_size=1) == hello_world_hash


@pytest.mark.parametrize("buffer_size", [0, -1])
def test_hash_file_rejects_non_positive_buffer_size(
    buffer_size: int,
    tmp_path: Path,
) -> None:
    content = b"important content that must be hashed"
    tmp_file = tmp_path / "important.txt"
    tmp_file.write_bytes(content)

    with pytest.raises(ValueError, match="buffer_size must be at least 1"):
        hash_file(tmp_file, buffer_size=buffer_size)

    expected = hashlib.sha256(content).hexdigest()
    assert expected != hashlib.sha256().hexdigest()
    assert hash_file(tmp_file, buffer_size=1) == expected
