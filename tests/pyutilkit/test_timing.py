from __future__ import annotations

from time import sleep

import pytest

from pyutilkit.timing import Stopwatch, Timing


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
        ({"nanoseconds": -1}, "-1ns"),
        ({"nanoseconds": 1, "microseconds": 1}, "1.0µs"),
        ({"nanoseconds": 1, "milliseconds": 1}, "1.0ms"),
        ({"nanoseconds": 1, "seconds": 1}, "1.00s"),
        ({"nanoseconds": 1, "days": 1}, "1d 00:00:00"),
        ({"seconds": 3601}, "01:00:01"),
        (
            {
                "nanoseconds": 1,
                "days": 1,
                "seconds": 1,
                "milliseconds": 1,
                "microseconds": 1,
            },
            "1d 00:00:01",
        ),
    ],
)
def test_timing_as_str(timings: dict[str, int], expected_str: str) -> None:
    assert str(Timing(**timings)) == expected_str


def test_negative_timing() -> None:
    timing = -Timing(nanoseconds=5)
    assert timing.nanoseconds == -5


@pytest.mark.parametrize(
    ("timings", "expected_bool"),
    [
        ({}, False),
        ({"nanoseconds": 1}, True),
        ({"nanoseconds": 0}, False),
    ],
)
def test_timing_as_bool(timings: dict[str, int], expected_bool: bool) -> None:
    assert bool(Timing(**timings)) is expected_bool


def test_timing_operators() -> None:
    timing = Timing(nanoseconds=5)
    assert timing + timing == Timing(nanoseconds=10)
    assert timing - timing == Timing(nanoseconds=0)
    assert timing.__radd__(timing) == Timing(nanoseconds=10)
    assert timing.__rsub__(timing) == Timing(nanoseconds=0)
    assert timing * 2 == Timing(nanoseconds=10)
    assert 2 * timing == Timing(nanoseconds=10)
    assert timing // 3 == Timing(nanoseconds=1)
    assert timing / 3 == Timing(nanoseconds=2)


def test_timing_operators_exceptions() -> None:
    timing = Timing(nanoseconds=5)
    with pytest.raises(TypeError):
        "1" * timing
    with pytest.raises(TypeError):
        1 + timing
    with pytest.raises(TypeError):
        1 - timing
    with pytest.raises(TypeError):
        timing * "1"
    with pytest.raises(TypeError):
        timing + 1
    with pytest.raises(TypeError):
        timing - 1
    with pytest.raises(TypeError):
        timing / "1"
    with pytest.raises(TypeError):
        timing // "1"


def test_stopwatch() -> None:
    stopwatch = Stopwatch()

    with pytest.raises(ZeroDivisionError):
        stopwatch.average  # noqa: B018

    assert not stopwatch

    with stopwatch:
        sleep(0.02)

    with stopwatch:
        sleep(0.02)

    assert len(stopwatch) == len(stopwatch.laps) == 2
    assert stopwatch.laps[0].nanoseconds > 16_000_000
    assert stopwatch.laps[1].nanoseconds > 16_000_000
    assert stopwatch.average.nanoseconds > 16_000_000
    assert stopwatch.min <= stopwatch.average <= stopwatch.max

    assert list(stopwatch) == stopwatch.laps
    assert stopwatch
