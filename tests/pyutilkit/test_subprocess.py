from __future__ import annotations

import pytest

from pyutilkit.subprocess import run_command
from pyutilkit.timing import Timing


def test_run_command() -> None:
    command = ["echo", "Hello, World!"]
    output = run_command(command)
    assert output.stdout == b"Hello, World!\n"
    assert output.stderr == b""
    assert output.returncode == 0
    assert output.elapsed > Timing(nanoseconds=0)
    assert output.pid > 0


def test_run_command_with_invalid_stdout() -> None:
    command = ["echo", "Hello, World!"]
    with pytest.raises(ValueError, match="stdout must be set to PIPE"):
        run_command(command, stdout=None)


def test_run_command_with_invalid_stderr() -> None:
    command = ["echo", "Hello, World!"]
    with pytest.raises(ValueError, match="stderr must be set to PIPE"):
        run_command(command, stderr=None)


def test_run_command_with_failing() -> None:
    command = ["false"]
    output = run_command(command)
    assert output.stdout == b""
    assert output.stderr == b""
    assert output.returncode != 0
    assert output.elapsed > Timing(nanoseconds=0)
    assert output.pid > 0
