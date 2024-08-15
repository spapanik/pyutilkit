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


def run_command(command: str | list[str], **kwargs: Any) -> ProcessOutput:
    if kwargs.setdefault("stdout", PIPE) != PIPE:
        msg = "stdout must be set to PIPE"
        raise ValueError(msg)
    if kwargs.setdefault("stderr", PIPE) != PIPE:
        msg = "stderr must be set to PIPE"
        raise ValueError(msg)

    stdout = []
    stderr = []
    stopwatch = Stopwatch()
    with stopwatch:
        process = Popen(command, **kwargs)  # noqa: S603

        for line in process.stdout or []:
            sys.stdout.buffer.write(line)
            sys.stdout.flush()
            stdout.append(line)

        for line in process.stderr or []:
            sys.stderr.buffer.write(line)
            sys.stderr.flush()
            stderr.append(line)

    with stopwatch:
        process.wait()

    return ProcessOutput(
        stdout=b"".join(stdout),
        stderr=b"".join(stderr),
        pid=process.pid,
        returncode=process.returncode,
        elapsed=stopwatch.elapsed,
    )
