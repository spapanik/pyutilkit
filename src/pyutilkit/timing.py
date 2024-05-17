from __future__ import annotations  # py3.9: remove this line

from dataclasses import dataclass
from time import perf_counter_ns
from types import TracebackType
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing_extensions import Self  # py3.10: import Self from typing


@dataclass(frozen=True, order=True)
class Timing:
    __slots__ = ("nanoseconds",)  # py3.9: remove this line

    nanoseconds: int

    def __init__(
        self,
        *,
        days: int = 0,
        seconds: int = 0,
        milliseconds: int = 0,
        microseconds: int = 0,
        nanoseconds: int = 0,
    ) -> None:
        total_nanoseconds = (
            nanoseconds
            + 1000 * microseconds
            + 1_000_000 * milliseconds
            + 1_000_000_000 * seconds
            + 86_400_000_000_000 * days
        )
        object.__setattr__(self, "nanoseconds", total_nanoseconds)

    def __str__(self) -> str:
        if self.nanoseconds < 1000:
            return f"{self.nanoseconds}ns"
        microseconds = self.nanoseconds / 1000
        if microseconds < 1000:
            return f"{microseconds:.1f}µs"
        milliseconds = microseconds / 1000
        if milliseconds < 1000:
            return f"{milliseconds:.1f}ms"
        seconds = milliseconds / 1000
        if seconds < 60:
            return f"{seconds:.2f}s"
        round_seconds = int(seconds)
        minutes, seconds = divmod(round_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        if hours < 24:
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        days, hours = divmod(hours, 24)
        return f"{days:,}d {hours:02d}:{minutes:02d}:{seconds:02d}"


class Stopwatch:
    _start: int
    timing: Timing

    def __init__(self) -> None:
        self._start = 0
        self.timing = Timing(nanoseconds=0)

    def __enter__(self) -> Self:
        self._start = perf_counter_ns()
        return self

    def __exit__(
        self,
        exc_type: type[Exception] | None,
        exc_value: Exception | None,
        traceback: TracebackType | None,
    ) -> None:
        _end = perf_counter_ns()
        self.timing = Timing(nanoseconds=_end - self._start)
