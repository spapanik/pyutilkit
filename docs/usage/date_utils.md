# Date Utilities Module

The `date_utils` module provides timezone-aware datetime utilities that simplify working with dates and times across different timezones. It handles common pitfalls like naive vs aware datetimes, ISO format parsing with Zulu timezone, and cross-platform timezone availability.

## Overview

Working with timezones in Python can be tricky. The `date_utils` module provides a consistent API for:

- Getting the current time in any timezone
- Parsing ISO format datetime strings (including Zulu timezone "Z")
- Converting Unix timestamps to timezone-aware datetimes
- Adding timezone info to naive datetimes
- Converting between timezones while preserving the actual moment in time

## Basic Usage

### Getting Current Time

```python
from pyutilkit.date_utils import now
from zoneinfo import ZoneInfo

# Get current time in UTC (default)
utc_time = now()
print(utc_time)  # 2024-01-15 10:30:00+00:00

# Get current time in specific timezone
tokyo_time = now(ZoneInfo("Asia/Tokyo"))
print(tokyo_time)  # 2024-01-15 19:30:00+09:00

london_time = now(ZoneInfo("Europe/London"))
print(london_time)  # 2024-01-15 10:30:00+00:00 (or +01:00 in summer)
```

### Parsing ISO Format Strings

```python
from pyutilkit.date_utils import from_iso
from zoneinfo import ZoneInfo

# Parse ISO string with Zulu timezone
dt = from_iso("2024-01-15T10:30:00Z")
print(dt)  # 2024-01-15 10:30:00+00:00

# Parse and convert to specific timezone
tokyo_dt = from_iso("2024-01-15T10:30:00Z", ZoneInfo("Asia/Tokyo"))
print(tokyo_dt)  # 2024-01-15 19:30:00+09:00

# Parse ISO string with explicit timezone offset
dt = from_iso("2024-01-15T10:30:00+05:30")
print(dt)  # 2024-01-15 05:00:00+00:00 (converted to UTC)
```

### Working with Timestamps

```python
from pyutilkit.date_utils import from_timestamp
from zoneinfo import ZoneInfo

# Convert Unix timestamp to datetime
epoch_utc = from_timestamp(0)
print(epoch_utc)  # 1970-01-01 00:00:00+00:00

# Convert to specific timezone
epoch_tokyo = from_timestamp(0, ZoneInfo("Asia/Tokyo"))
print(epoch_tokyo)  # 1970-01-01 09:00:00+09:00

# Current timestamp
import time
current = from_timestamp(time.time(), ZoneInfo("America/New_York"))
print(current)
```

## Advanced Patterns

### Timezone Conversion

```python
from pyutilkit.date_utils import convert_timezone, add_timezone
from zoneinfo import ZoneInfo
from datetime import datetime

# Convert between timezones (preserves the actual moment)
tokyo_time = datetime(2024, 1, 15, 19, 30, tzinfo=ZoneInfo("Asia/Tokyo"))
london_time = convert_timezone(tokyo_time, ZoneInfo("Europe/London"))
print(london_time)  # 2024-01-15 10:30:00+00:00

# Add timezone to naive datetime
naive_dt = datetime(2024, 1, 15, 10, 30)
aware_dt = add_timezone(naive_dt, ZoneInfo("UTC"))
print(aware_dt)  # 2024-01-15 10:30:00+00:00
```

### Handling Naive vs Aware Datetimes

```python
from pyutilkit.date_utils import add_timezone, convert_timezone
from zoneinfo import ZoneInfo
from datetime import datetime

# This will raise ValueError - can't add timezone to aware datetime
aware_dt = datetime(2024, 1, 15, 10, 30, tzinfo=ZoneInfo("UTC"))
try:
    add_timezone(aware_dt, ZoneInfo("Asia/Tokyo"))
except ValueError as e:
    print(f"Error: {e}")  # Error: 2024-01-15 10:30:00+00:00 is already tz-aware

# This will raise ValueError - can't convert naive datetime
naive_dt = datetime(2024, 1, 15, 10, 30)
try:
    convert_timezone(naive_dt, ZoneInfo("Asia/Tokyo"))
except ValueError as e:
    print(f"Error: {e}")  # Error: 2024-01-15 10:30:00 is a naive datetime
```

### Getting Available Timezones

```python
from pyutilkit.date_utils import get_timezones

# Get all available timezones (filtered for cross-platform compatibility)
timezones = get_timezones()
print(f"Available timezones: {len(timezones)}")

# Check if a timezone is available
if "Asia/Tokyo" in timezones:
    print("Tokyo timezone is available")
```

## Real-World Examples

### API Timestamp Handler

```python
from pyutilkit.date_utils import from_iso, now, convert_timezone
from zoneinfo import ZoneInfo


def parse_api_timestamp(timestamp_str: str, user_timezone: str = "UTC") -> str:
    """Parse API timestamp and convert to user's timezone.

    Args:
        timestamp_str: ISO format timestamp from API
        user_timezone: Target timezone string

    Returns:
        Formatted datetime string in user's timezone
    """
    # Parse the timestamp (handles Zulu timezone)
    utc_dt = from_iso(timestamp_str)

    # Convert to user's timezone
    user_tz = ZoneInfo(user_timezone)
    local_dt = convert_timezone(utc_dt, user_tz)

    # Format for display
    return local_dt.strftime("%Y-%m-%d %H:%M:%S %Z")


# Example usage
api_timestamp = "2024-01-15T10:30:00Z"
print(parse_api_timestamp(api_timestamp, "America/New_York"))
# Output: 2024-01-15 05:30:00 EST

print(parse_api_timestamp(api_timestamp, "Asia/Tokyo"))
# Output: 2024-01-15 19:30:00 JST
```

### Scheduled Task Manager

```python
from pyutilkit.date_utils import now, from_iso, convert_timezone
from zoneinfo import ZoneInfo


class TaskScheduler:
    """Schedule tasks across different timezones."""

    def __init__(self):
        self.tasks = []

    def schedule_task(self, name: str, scheduled_time: str, timezone: str):
        """Schedule a task with timezone-aware time.

        Args:
            name: Task name
            scheduled_time: ISO format time string
            timezone: Timezone for the scheduled time
        """
        # Parse the scheduled time in its timezone
        tz = ZoneInfo(timezone)
        local_time = from_iso(scheduled_time, tz)

        # Convert to UTC for storage/comparison
        utc_time = convert_timezone(local_time, ZoneInfo("UTC"))

        self.tasks.append({
            'name': name,
            'scheduled_utc': utc_time,
            'timezone': timezone
        })

    def get_due_tasks(self):
        """Get tasks that are due now (in UTC)."""
        current_utc = now(ZoneInfo("UTC"))
        return [
            task for task in self.tasks
            if task['scheduled_utc'] <= current_utc
        ]


# Example usage
scheduler = TaskScheduler()
scheduler.schedule_task(
    "Daily Report",
    "2024-01-15T09:00:00",
    "America/New_York"
)
scheduler.schedule_task(
    "Team Standup",
    "2024-01-15T10:00:00Z",
    "UTC"
)

due_tasks = scheduler.get_due_tasks()
for task in due_tasks:
    print(f"Task '{task['name']}' is due!")
```

### Log Timestamp Normalizer

```python
from pyutilkit.date_utils import from_iso, convert_timezone
from zoneinfo import ZoneInfo


def normalize_log_timestamps(log_entries: list[dict]) -> list[dict]:
    """Normalize log timestamps from different sources to UTC.

    Args:
        log_entries: List of log entries with 'timestamp' and 'source_timezone'

    Returns:
        Log entries with normalized UTC timestamps
    """
    normalized = []
    for entry in log_entries:
        # Parse timestamp in source timezone
        source_tz = ZoneInfo(entry['source_timezone'])
        local_dt = from_iso(entry['timestamp'], source_tz)

        # Convert to UTC
        utc_dt = convert_timezone(local_dt, ZoneInfo("UTC"))

        normalized.append({
            **entry,
            'timestamp_utc': utc_dt.isoformat(),
            'original_timestamp': entry['timestamp']
        })

    return normalized


# Example: Logs from servers in different timezones
logs = [
    {
        'message': 'Server started',
        'timestamp': '2024-01-15T10:30:00',
        'source_timezone': 'US/Eastern'
    },
    {
        'message': 'Deployment complete',
        'timestamp': '2024-01-15T18:45:00+09:00',
        'source_timezone': 'Asia/Tokyo'
    },
    {
        'message': 'Backup finished',
        'timestamp': '2024-01-15T15:20:00Z',
        'source_timezone': 'UTC'
    }
]

normalized_logs = normalize_log_timestamps(logs)
for log in sorted(normalized_logs, key=lambda x: x['timestamp_utc']):
    print(f"{log['timestamp_utc']} - {log['message']}")
```

## Common Pitfalls

!!! warning "Naive vs Aware Datetimes"
    Always ensure your datetimes are timezone-aware before converting. Use `add_timezone()` for naive datetimes and `convert_timezone()` for aware datetimes. Mixing them up will raise `ValueError`.

!!! warning "DST Transitions"
    Be careful during Daylight Saving Time transitions. The same wall-clock time might occur twice or not at all. The `zoneinfo` module handles this, but be aware of potential ambiguities.

!!! tip "Always Store in UTC"
    Store timestamps in UTC and convert to local time only for display. This avoids confusion and makes comparisons straightforward.

!!! tip "Use from_iso() for API Responses"
    When parsing timestamps from APIs, always use `from_iso()` instead of `datetime.fromisoformat()` directly. It properly handles the Zulu timezone ("Z") which is valid ISO 8601 but not supported by Python's standard parser.

## API Reference

::: pyutilkit.date_utils
    handler: python
    options:
      show_root_heading: true
      show_source: false
      members:
        - now
        - from_iso
        - from_timestamp
        - add_timezone
        - convert_timezone
        - get_timezones
        - UTC
