from __future__ import annotations

import pytest

from pyutilkit.timing import Timing


@pytest.mark.parametrize(
    ("timings", "expected_nanoseconds"),
    [
        ({}, 0),
        ({"nanoseconds": 1}, 1),
        ({"nanoseconds": 1, "days": 1}, 86_400_000_000_001),
        ({"nanoseconds": 1, "seconds": 1}, 1_000_000_001),
        ({"nanoseconds": 1, "milliseconds": 1}, 1_000_001),
        ({"nanoseconds": 1, "microseconds": 1}, 1_001),
        (
            {
                "nanoseconds": 1,
                "days": 1,
                "seconds": 1,
                "milliseconds": 1,
                "microseconds": 1,
            },
            86_401_001_001_001,
        ),
    ],
)
def test_timing(timings: dict[str, int], expected_nanoseconds: int) -> None:
    assert Timing(**timings).nanoseconds == expected_nanoseconds


@pytest.mark.parametrize(
    ("timings", "expected_str"),
    [
        ({}, "0ns"),
        ({"nanoseconds": 1}, "1ns"),
        ({"nanoseconds": 1, "microseconds": 1}, "1.0µs"),
        ({"nanoseconds": 1, "milliseconds": 1}, "1.0ms"),
        ({"nanoseconds": 1, "seconds": 1}, "1.00s"),
        ({"nanoseconds": 1, "days": 1}, "86,400.00s"),
        (
            {
                "nanoseconds": 1,
                "days": 1,
                "seconds": 1,
                "milliseconds": 1,
                "microseconds": 1,
            },
            "86,401.00s",
        ),
    ],
)
def test_timing_as_str(timings: dict[str, int], expected_str: str) -> None:
    assert str(Timing(**timings)) == expected_str
