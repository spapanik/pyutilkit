# Timing Module

The `timing` module provides high-precision timing utilities with human-readable output formatting. It includes a `Timing` class for representing durations and a `Stopwatch` class for measuring execution time with lap tracking.

## Overview

Measuring and displaying execution time is common in:
- Performance profiling
- Benchmarking code
- Monitoring SLAs
- Logging operation durations
- Debugging slow operations

The `timing` module makes this easy with:
- Nanosecond precision using `perf_counter_ns()`
- Automatic human-readable formatting
- Arithmetic operations on durations
- Lap tracking for repeated measurements
- Context manager support for clean syntax

## Basic Usage

### Creating Timing Objects

```python
from pyutilkit.timing import Timing

# Create timing from different units
t1 = Timing(nanoseconds=1500)
t2 = Timing(microseconds=500)
t3 = Timing(milliseconds=250)
t4 = Timing(seconds=5)
t5 = Timing(minutes=2, seconds=30)
t6 = Timing(hours=1, minutes=30, seconds=45)
t7 = Timing(days=2, hours=3)

print(t1)  # 1.5µs
print(t2)  # 500.0µs
print(t3)  # 250.0ms
print(t4)  # 5.00s
print(t5)  # 02:30:00
print(t6)  # 01:30:45
print(t7)  # 2d 03:00:00
```

### Human-Readable Formatting

The `Timing` class automatically chooses the best unit for display:

```python
from pyutilkit.timing import Timing

# Automatic unit selection
print(Timing(nanoseconds=0))           # 0ns
print(Timing(nanoseconds=100))         # 100ns
print(Timing(nanoseconds=1500))        # 1.5µs
print(Timing(microseconds=500))        # 500.0µs
print(Timing(milliseconds=250))        # 250.0ms
print(Timing(seconds=5))               # 5.00s
print(Timing(seconds=90))              # 01:30:00
print(Timing(hours=25))                # 1d 01:00:00
print(Timing(days=10))                 # 10d 00:00:00

# Negative times (for differences)
diff = Timing(seconds=-5)
print(diff)  # -5.00s
```

### Arithmetic Operations

```python
from pyutilkit.timing import Timing

# Addition
t1 = Timing(seconds=5)
t2 = Timing(seconds=3)
total = t1 + t2
print(total)  # 8.00s

# Subtraction
diff = t1 - t2
print(diff)  # 2.00s

# Multiplication by integer
doubled = t1 * 2
print(doubled)  # 10.00s

# Division by integer
halved = t1 // 2
print(halved)  # 2.50s

# Negation
negative = -t1
print(negative)  # -5.00s

# Comparison
t3 = Timing(seconds=5)
print(t1 == t3)  # True
print(t1 > t2)   # True
print(t1 < Timing(seconds=10))  # True
```

## Stopwatch

The `Stopwatch` class provides convenient timing measurement with context manager support and lap tracking.

### Basic Stopwatch Usage

```python
from pyutilkit.timing import Stopwatch
import time

# Using as context manager
stopwatch = Stopwatch()

with stopwatch:
    time.sleep(0.1)  # Simulate work

print(f"Elapsed: {stopwatch.elapsed}")  # Elapsed: ~100.0ms
print(f"Laps: {len(stopwatch)}")        # Laps: 1
```

### Multiple Laps

```python
from pyutilkit.timing import Stopwatch
import time

stopwatch = Stopwatch()

# First operation
with stopwatch:
    time.sleep(0.05)

# Second operation
with stopwatch:
    time.sleep(0.1)

# Third operation
with stopwatch:
    time.sleep(0.075)

print(f"Total elapsed: {stopwatch.elapsed}")    # ~225.0ms
print(f"Number of laps: {len(stopwatch)}")      # 3
print(f"Average lap: {stopwatch.average}")      # ~75.0ms
print(f"Fastest lap: {stopwatch.min}")          # ~50.0ms
print(f"Slowest lap: {stopwatch.max}")          # ~100.0ms

# Iterate through laps
for i, lap in enumerate(stopwatch, 1):
    print(f"Lap {i}: {lap}")
```

### Resetting Stopwatch

```python
from pyutilkit.timing import Stopwatch
import time

stopwatch = Stopwatch()

with stopwatch:
    time.sleep(0.1)

print(f"First measurement: {stopwatch.elapsed}")  # ~100.0ms

# Reset and measure again
stopwatch.reset()

with stopwatch:
    time.sleep(0.05)

print(f"After reset: {stopwatch.elapsed}")  # ~50.0ms
print(f"Laps after reset: {len(stopwatch)}")  # 1
```

### Boolean Check

```python
from pyutilkit.timing import Stopwatch

stopwatch = Stopwatch()

# Empty stopwatch is falsy
if not stopwatch:
    print("No measurements yet")

# After measurement, it's truthy
with stopwatch:
    pass

if stopwatch:
    print(f"Measured: {stopwatch.elapsed}")
```

## Real-World Examples

### Function Decorator for Timing

```python
from pyutilkit.timing import Stopwatch, Timing
from functools import wraps
from typing import Callable, TypeVar
import logging

logger = logging.getLogger(__name__)
T = TypeVar('T')


def timed(func: Callable[..., T]) -> Callable[..., T]:
    """Decorator to measure function execution time."""

    @wraps(func)
    def wrapper(*args, **kwargs) -> T:
        stopwatch = Stopwatch()
        with stopwatch:
            result = func(*args, **kwargs)

        logger.info(
            f"{func.__name__} executed in {stopwatch.elapsed}"
        )
        return result

    return wrapper


# Example usage
@timed
def slow_function():
    """Simulate a slow operation."""
    import time
    time.sleep(0.5)
    return "Done"


result = slow_function()
# Logs: slow_function executed in 500.2ms
```

### Performance Benchmark

```python
from pyutilkit.timing import Stopwatch
import time
from typing import Callable


def benchmark(func: Callable, iterations: int = 100) -> dict:
    """Benchmark a function over multiple iterations.

    Args:
        func: Function to benchmark
        iterations: Number of iterations

    Returns:
        Dictionary with benchmark statistics
    """
    stopwatch = Stopwatch()

    for _ in range(iterations):
        with stopwatch:
            func()

    return {
        'total': stopwatch.elapsed,
        'average': stopwatch.average,
        'min': stopwatch.min,
        'max': stopwatch.max,
        'iterations': iterations,
    }


# Example: Compare different string concatenation methods
def concat_with_plus():
    s = ""
    for i in range(1000):
        s += str(i)


def concat_with_join():
    parts = []
    for i in range(1000):
        parts.append(str(i))
    "".join(parts)


print("String concatenation with +:")
stats = benchmark(concat_with_plus, 100)
print(f"  Average: {stats['average']}")
print(f"  Min: {stats['min']}")
print(f"  Max: {stats['max']}")

print("\nString concatenation with join:")
stats = benchmark(concat_with_join, 100)
print(f"  Average: {stats['average']}")
print(f"  Min: {stats['min']}")
print(f"  Max: {stats['max']}")
```

### API Response Time Monitor

```python
from pyutilkit.timing import Stopwatch
import requests
from dataclasses import dataclass
from datetime import datetime


@dataclass
class APIResponse:
    """API response with timing information."""
    url: str
    status_code: int
    elapsed: Timing
    timestamp: datetime


class APIMonitor:
    """Monitor API response times."""

    def __init__(self):
        self.responses: list[APIResponse] = []

    def call_api(self, url: str, timeout: int = 30) -> APIResponse:
        """Call API and measure response time."""
        stopwatch = Stopwatch()

        with stopwatch:
            response = requests.get(url, timeout=timeout)

        api_response = APIResponse(
            url=url,
            status_code=response.status_code,
            elapsed=stopwatch.elapsed,
            timestamp=datetime.now()
        )

        self.responses.append(api_response)
        return api_response

    def get_statistics(self) -> dict:
        """Get response time statistics."""
        if not self.responses:
            return {}

        elapsed_times = [r.elapsed for r in self.responses]

        return {
            'total_requests': len(self.responses),
            'total_time': sum(elapsed_times),
            'average_time': sum(elapsed_times) // len(elapsed_times),
            'min_time': min(elapsed_times),
            'max_time': max(elapsed_times),
            'success_rate': sum(
                1 for r in self.responses if r.status_code == 200
            ) / len(self.responses) * 100,
        }


# Example usage
monitor = APIMonitor()

# Make several API calls
urls = [
    "https://httpbin.org/delay/1",
    "https://httpbin.org/delay/2",
    "https://httpbin.org/status/200",
]

for url in urls:
    response = monitor.call_api(url)
    print(f"{url}: {response.elapsed} (status: {response.status_code})")

# Get statistics
stats = monitor.get_statistics()
print(f"\nStatistics:")
print(f"  Total requests: {stats['total_requests']}")
print(f"  Average time: {stats['average_time']}")
print(f"  Min time: {stats['min_time']}")
print(f"  Max time: {stats['max_time']}")
print(f"  Success rate: {stats['success_rate']:.1f}%")
```

### Task Scheduler with Timeout

```python
from pyutilkit.timing import Stopwatch, Timing
from typing import Callable
import time


class TaskWithTimeout:
    """Execute tasks with timeout enforcement."""

    def __init__(self, timeout: Timing):
        self.timeout = timeout

    def execute(self, task: Callable, *args, **kwargs) -> tuple[bool, Timing]:
        """Execute task with timeout.

        Args:
            task: Function to execute
            *args: Positional arguments for task
            **kwargs: Keyword arguments for task

        Returns:
            Tuple of (success, elapsed_time)
        """
        stopwatch = Stopwatch()

        try:
            with stopwatch:
                result = task(*args, **kwargs)

                # Check if we exceeded timeout
                if stopwatch.elapsed > self.timeout:
                    return False, stopwatch.elapsed

            return True, stopwatch.elapsed

        except Exception as e:
            return False, stopwatch.elapsed


# Example usage
def fast_task():
    """Task that completes quickly."""
    time.sleep(0.1)
    return "Fast result"


def slow_task():
    """Task that takes too long."""
    time.sleep(2)
    return "Slow result"


# Set 1 second timeout
timeout = Timing(seconds=1)
executor = TaskWithTimeout(timeout)

# Fast task succeeds
success, elapsed = executor.execute(fast_task)
print(f"Fast task: {'✓' if success else '✗'} ({elapsed})")
# Output: Fast task: ✓ (100.5ms)

# Slow task times out
success, elapsed = executor.execute(slow_task)
print(f"Slow task: {'✓' if success else '✗'} ({elapsed})")
# Output: Slow task: ✗ (2.00s)
```

### Batch Processing Progress Tracker

```python
from pyutilkit.timing import Stopwatch, Timing
from typing import Iterable, TypeVar
import sys

T = TypeVar('T')


def process_with_progress(
    items: Iterable[T],
    processor: Callable[[T], None],
    batch_size: int = 100
) -> Timing:
    """Process items with progress tracking and timing.

    Args:
        items: Items to process
        processor: Function to process each item
        batch_size: Report progress every N items

    Returns:
        Total elapsed time
    """
    stopwatch = Stopwatch()
    count = 0

    for item in items:
        with stopwatch:
            processor(item)

        count += 1

        # Report progress periodically
        if count % batch_size == 0:
            avg_time = stopwatch.average
            estimated_remaining = avg_time * (count // batch_size)
            print(
                f"\rProcessed {count} items | "
                f"Avg: {avg_time} | "
                f"Elapsed: {stopwatch.elapsed}",
                end="",
                flush=True
            )

    print(f"\nCompleted {count} items in {stopwatch.elapsed}")
    return stopwatch.elapsed


# Example usage
def process_item(item: int):
    """Simulate processing an item."""
    import time
    time.sleep(0.001)  # 1ms per item


items = range(1000)
total_time = process_with_progress(items, process_item, batch_size=100)
print(f"Total processing time: {total_time}")
```

### SLA Compliance Checker

```python
from pyutilkit.timing import Stopwatch, Timing
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SLARequirement:
    """Service Level Agreement requirement."""
    name: str
    max_response_time: Timing
    target_success_rate: float  # percentage


@dataclass
class SLAResult:
    """SLA compliance result."""
    requirement: SLARequirement
    compliant: bool
    actual_response_time: Timing
    actual_success_rate: float


class SLAMonitor:
    """Monitor SLA compliance."""

    def __init__(self):
        self.measurements: list[tuple[Timing, bool]] = []

    def record_measurement(self, response_time: Timing, success: bool):
        """Record a service measurement."""
        self.measurements.append((response_time, success))

    def check_compliance(self, sla: SLARequirement) -> SLAResult:
        """Check if service meets SLA requirements."""
        if not self.measurements:
            return SLAResult(
                requirement=sla,
                compliant=False,
                actual_response_time=Timing(),
                actual_success_rate=0.0
            )

        # Calculate metrics
        response_times = [m[0] for m in self.measurements]
        successes = sum(1 for m in self.measurements if m[1])
        total = len(self.measurements)

        avg_response = sum(response_times) // total
        success_rate = (successes / total) * 100

        # Check compliance
        time_compliant = avg_response <= sla.max_response_time
        rate_compliant = success_rate >= sla.target_success_rate
        compliant = time_compliant and rate_compliant

        return SLAResult(
            requirement=sla,
            compliant=compliant,
            actual_response_time=avg_response,
            actual_success_rate=success_rate
        )

    def report(self, sla: SLARequirement) -> str:
        """Generate SLA compliance report."""
        result = self.check_compliance(sla)

        status = "✓ COMPLIANT" if result.compliant else "✗ NON-COMPLIANT"
        status_color = "GREEN" if result.compliant else "RED"

        report = f"""
SLA Report: {sla.name}
{'='*50}
Status: {status}

Requirements:
  - Max Response Time: {sla.max_response_time}
  - Target Success Rate: {sla.target_success_rate:.1f}%

Actual Performance:
  - Avg Response Time: {result.actual_response_time}
  - Actual Success Rate: {result.actual_success_rate:.1f}%

Measurements: {len(self.measurements)}
"""
        return report


# Example usage
monitor = SLAMonitor()

# Simulate measurements
import random
import time

for _ in range(100):
    # Simulate response time (mostly fast, occasionally slow)
    response_ms = random.gauss(100, 30)
    response_time = Timing(milliseconds=max(10, int(response_ms)))

    # Simulate success/failure (95% success rate)
    success = random.random() < 0.95

    monitor.record_measurement(response_time, success)

# Define SLA
sla = SLARequirement(
    name="API Response Time",
    max_response_time=Timing(milliseconds=150),
    target_success_rate=95.0
)

# Check and report
print(monitor.report(sla))
```

## Common Pitfalls

!!! warning "Context Manager Usage"
    Always use `Stopwatch` as a context manager (`with stopwatch:`). Manually calling `__enter__` and `__exit__` can lead to incorrect measurements.

!!! warning "Division by Zero"
    Calling `stopwatch.average` when no laps have been recorded raises `ZeroDivisionError`. Always check `len(stopwatch)` first or handle the exception.

!!! tip "Use Appropriate Precision"
    For most applications, millisecond precision is sufficient. Use nanosecond precision only when you need extreme accuracy (e.g., benchmarking very fast operations).

!!! tip "Account for Overhead"
    The timing itself has minimal overhead, but be aware that printing or logging during measurement can affect results. Keep measurement code separate from reporting code.

## API Reference

::: pyutilkit.timing
    handler: python
    options:
      show_root_heading: true
      show_source: false
      members:
        - Timing
        - Stopwatch
