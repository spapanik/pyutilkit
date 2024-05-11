from dataclasses import dataclass


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
        return f"{seconds:,.2f}s"
