from __future__ import annotations

import sys
from dataclasses import dataclass
from queue import SimpleQueue
from subprocess import PIPE, Popen
from threading import Thread
from typing import TYPE_CHECKING, cast

from pyutilkit.timing import Stopwatch, Timing

if TYPE_CHECKING:
    from pathlib import Path
    from typing import BinaryIO


@dataclass(frozen=True)
class ProcessOutput:
    stdout: bytes
    stderr: bytes
    pid: int
    returncode: int
    elapsed: Timing


def _write_output(stream: BinaryIO, line: bytes) -> None:
    stream.write(line)
    stream.flush()


def _drain_pipe(
    pipe: BinaryIO,
    output: BinaryIO | None,
    captured: list[bytes],
    errors: SimpleQueue[Exception],
) -> None:
    echo = output is not None
    for line in pipe:
        captured.append(line)
        if not echo:
            continue
        try:
            _write_output(output, line)
        except Exception as exc:  # noqa: BLE001
            errors.put(exc)
            echo = False


def _validate_command(command: object) -> list[str]:
    if not isinstance(command, list):
        msg = "command must be a list of argument strings"
        raise TypeError(msg)
    return cast("list[str]", command)


def run_command(
    command: list[str],
    cwd: str | Path | None = None,
    env: dict[str, str] | None = None,
) -> ProcessOutput:
    command = _validate_command(command)

    stdout: list[bytes] = []
    stderr: list[bytes] = []
    errors: SimpleQueue[Exception] = SimpleQueue()
    stopwatch = Stopwatch()
    with (
        stopwatch,
        Popen(  # noqa: S603
            command, stdout=PIPE, stderr=PIPE, cwd=cwd, env=env
        ) as process,
    ):
        stdout_pipe = cast("BinaryIO", process.stdout)
        stderr_pipe = cast("BinaryIO", process.stderr)
        readers = (
            Thread(
                target=_drain_pipe,
                args=(stdout_pipe, getattr(sys.stdout, "buffer", None), stdout, errors),
                name=f"pyutilkit-stdout-{process.pid}",
            ),
            Thread(
                target=_drain_pipe,
                args=(stderr_pipe, getattr(sys.stderr, "buffer", None), stderr, errors),
                name=f"pyutilkit-stderr-{process.pid}",
            ),
        )
        for reader in readers:
            reader.start()

        process.wait()
        for reader in readers:
            reader.join()

    if not errors.empty():
        raise errors.get()

    return ProcessOutput(
        stdout=b"".join(stdout),
        stderr=b"".join(stderr),
        pid=process.pid,
        returncode=process.returncode,
        elapsed=stopwatch.elapsed,
    )
