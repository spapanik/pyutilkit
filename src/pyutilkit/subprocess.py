from __future__ import annotations

import sys
from dataclasses import dataclass
from subprocess import PIPE, Popen
from typing import Any

from pyutilkit.timing import Stopwatch, Timing


@dataclass(frozen=True)
class ProcessOutput:
    stdout: bytes
    stderr: bytes
    pid: int
    returncode: int
    elapsed: Timing


def run_command(  # type: ignore[misc]
    command: str | list[str], **kwargs: Any  # noqa: ANN401
) -> ProcessOutput:
    if kwargs.setdefault("stdout", PIPE) != PIPE:  # type: ignore[misc]
        msg = "stdout must be set to PIPE"
        raise ValueError(msg)
    if kwargs.setdefault("stderr", PIPE) != PIPE:  # type: ignore[misc]
        msg = "stderr must be set to PIPE"
        raise ValueError(msg)

    stdout = []
    stderr = []
    stopwatch = Stopwatch()
    with stopwatch:
        process = Popen(command, **kwargs)  # type: ignore[misc]  # noqa: S603

        for line in process.stdout or []:
            sys.stdout.buffer.write(line)  # type: ignore[misc]
            sys.stdout.flush()
            stdout.append(line)

        for line in process.stderr or []:
            sys.stderr.buffer.write(line)  # type: ignore[misc]
            sys.stderr.flush()
            stderr.append(line)

    with stopwatch:
        process.wait()

    return ProcessOutput(
        stdout=b"".join(stdout),
        stderr=b"".join(stderr),
        pid=process.pid,
        returncode=process.returncode,  # type: ignore[misc]
        elapsed=stopwatch.elapsed,
    )
