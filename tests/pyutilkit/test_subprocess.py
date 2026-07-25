from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import cast
from unittest import mock

import pytest

import pyutilkit.subprocess as subprocess_module
from pyutilkit.subprocess import run_command
from pyutilkit.timing import Timing


def test_run_command() -> None:
    command = [
        sys.executable,
        "-c",
        "import sys; sys.stdout.buffer.write(b'Hello, World!\\n')",
    ]
    output = run_command(command)
    assert output.stdout == b"Hello, World!\n"
    assert output.stderr == b""
    assert output.returncode == 0
    assert output.elapsed > Timing(nanoseconds=0)
    assert output.pid > 0


def test_run_command_with_failing() -> None:
    command = [sys.executable, "-c", "raise SystemExit(1)"]
    output = run_command(command)
    assert output.stdout == b""
    assert output.stderr == b""
    assert output.returncode != 0
    assert output.elapsed > Timing(nanoseconds=0)
    assert output.pid > 0


def test_run_command_with_stderr() -> None:
    command = [
        sys.executable,
        "-c",
        (
            "import sys; sys.stderr.buffer.write(b'error\\n'); "
            "sys.stderr.buffer.flush(); raise SystemExit(1)"
        ),
    ]
    output = run_command(command)
    assert output.stdout == b""
    assert output.stderr == b"error\n"
    assert output.returncode != 0
    assert output.elapsed > Timing(nanoseconds=0)
    assert output.pid > 0


def test_run_command_preserves_native_line_endings() -> None:
    r"""`run_command` captures raw bytes, so a child's text-mode newlines survive.

    On Windows a child's `print()` emits `\r\n`; the output must not be
    normalised to `\n`.
    """
    command = [sys.executable, "-c", "print('Hello, World!')"]
    output = run_command(command)
    assert output.stdout == b"Hello, World!" + os.linesep.encode()


def test_run_command_rejects_string_commands() -> None:
    command = cast("list[str]", "echo 'Hello from shell'")
    with pytest.raises(TypeError, match="command must be a list of argument strings"):
        run_command(command)


@pytest.mark.parametrize("flood_stream", ["stdout", "stderr"])
def test_run_command_drains_pipes_concurrently(flood_stream: str) -> None:
    other_stream = "stderr" if flood_stream == "stdout" else "stdout"
    child_code = (
        "import sys; "
        f"sys.{flood_stream}.buffer.write(b'x' * 1_000_000); "
        f"sys.{flood_stream}.flush(); "
        f"sys.{other_stream}.buffer.write(b'done\\n'); "
        f"sys.{other_stream}.flush()"
    )
    expected_stdout = "b'x' * 1_000_000" if flood_stream == "stdout" else "b'done\\n'"
    expected_stderr = "b'x' * 1_000_000" if flood_stream == "stderr" else "b'done\\n'"
    probe = (
        "import sys\n"
        "from pyutilkit.subprocess import run_command\n"
        f"output = run_command([sys.executable, '-c', {child_code!r}])\n"
        f"assert output.stdout == {expected_stdout}\n"
        f"assert output.stderr == {expected_stderr}\n"
    )
    project_root = Path(__file__).parents[2]
    env = os.environ.copy()
    env["PYTHONPATH"] = str(project_root / "src")

    completed = subprocess.run(  # noqa: S603
        [sys.executable, "-c", probe],
        cwd=project_root,
        env=env,
        capture_output=True,
        timeout=10,
        check=False,
    )

    assert completed.returncode == 0, completed.stderr.decode()


@pytest.mark.parametrize("stream_name", ["stdout", "stderr"])
def test_run_command_streams_before_process_exit(
    stream_name: str,
    tmp_path: Path,
) -> None:
    completion_marker = tmp_path / f"{stream_name}-complete"
    child_code = (
        "import pathlib, sys, time; "
        f"sys.{stream_name}.buffer.write(b'ready\\n'); "
        f"sys.{stream_name}.buffer.flush(); "
        "time.sleep(0.2); "
        f"pathlib.Path({str(completion_marker)!r}).write_text('done'); "
        f"sys.{stream_name}.buffer.write(b'after\\n'); "
        f"sys.{stream_name}.buffer.flush()"
    )
    marker_states: list[bool] = []

    def observe_output(stream: object, line: bytes) -> None:
        del stream, line
        marker_states.append(completion_marker.exists())

    with mock.patch.object(subprocess_module, "_write_output", observe_output):
        output = run_command([sys.executable, "-c", child_code])

    expected = b"ready\nafter\n"
    assert output.stdout == (expected if stream_name == "stdout" else b"")
    assert output.stderr == (expected if stream_name == "stderr" else b"")
    assert output.elapsed >= Timing(milliseconds=200)
    assert marker_states == [False, True]
    assert completion_marker.read_text() == "done"


def test_run_command_reaps_process_before_propagating_echo_error(
    tmp_path: Path,
) -> None:
    completion_marker = tmp_path / "complete"
    child_code = (
        "import pathlib, sys, time; "
        "print('ready', flush=True); "
        "time.sleep(0.2); "
        f"pathlib.Path({str(completion_marker)!r}).write_text('done'); "
        "print('after', flush=True)"
    )

    with (
        mock.patch.object(
            subprocess_module,
            "_write_output",
            side_effect=BrokenPipeError("parent output is closed"),
        ),
        pytest.raises(BrokenPipeError, match="parent output is closed"),
    ):
        run_command([sys.executable, "-c", child_code])

    assert completion_marker.read_text() == "done"
