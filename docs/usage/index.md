# Usage Guide

Welcome to the pyutilkit usage guide! This section provides comprehensive documentation and practical examples for all modules in the library.

## Quick Reference

| Module | Purpose | Key Features |
|--------|---------|--------------|
| [Classes](classes.md) | Design patterns | Thread-safe Singleton implementation |
| [Date Utilities](date_utils.md) | Timezone-aware datetime handling | ISO parsing, timezone conversion, cross-platform support |
| [Files](files.md) | File operations & error handling | Exception decorator, SHA-256 file hashing |
| [Subprocess](subprocess.md) | Enhanced command execution | Real-time output, timing, structured results |
| [Terminal](term.md) | Terminal formatting | ANSI colors, TTY detection, smart output |
| [Timing](timing.md) | High-precision timing | Human-readable durations, lap tracking, stopwatch |

## Getting Started

### Installation

First, install pyutilkit:

```bash
pip install pyutilkit
```

Or with uv (recommended):

```bash
uv pip install pyutilkit
```

### Basic Import

```python
# Import specific modules
from pyutilkit.date_utils import now, from_iso
from pyutilkit.timing import Stopwatch, Timing
from pyutilkit.term import SGRString, SGRCodes
from pyutilkit.files import handle_exceptions, hash_file
from pyutilkit.subprocess import run_command
from pyutilkit.classes import Singleton
```

## Common Use Cases

### 🕐 Working with Timezones

Need to handle timestamps from APIs across different timezones?

```python
from pyutilkit.date_utils import from_iso, convert_timezone
from zoneinfo import ZoneInfo

# Parse API timestamp and convert to local timezone
api_timestamp = "2024-01-15T10:30:00Z"
utc_time = from_iso(api_timestamp)
local_time = convert_timezone(utc_time, ZoneInfo("America/New_York"))
print(local_time)  # 2024-01-15 05:30:00-05:00
```

→ See [Date Utilities Guide](date_utils.md) for more examples

### ⏱️ Measuring Performance

Want to benchmark your code or track operation durations?

```python
from pyutilkit.timing import Stopwatch

stopwatch = Stopwatch()
with stopwatch:
    # Your code here
    result = expensive_operation()

print(f"Operation took {stopwatch.elapsed}")
```

→ See [Timing Guide](timing.md) for advanced patterns

### 🎨 Colorful CLI Output

Building a command-line tool with formatted output?

```python
from pyutilkit.term import SGRString, SGRCodes

success = SGRString("✓ Success", params=[SGRCodes.GREEN, SGRCodes.BOLD])
error = SGRString("✗ Failed", params=[SGRCodes.RED], is_error=True)

success.print()  # Green bold text
error.print()    # Red text to stderr
```

→ See [Terminal Guide](term.md) for styling options

### 🛡️ Graceful Error Handling

Need robust error handling without cluttering your code?

```python
from pyutilkit.files import handle_exceptions

@handle_exceptions(exceptions=(ValueError, KeyError), default=None)
def safe_parse(data: dict) -> str | None:
    return data['key']

result = safe_parse({})  # Returns None instead of raising KeyError
```

→ See [Files Guide](files.md) for more patterns

### 🚀 Running Commands

Execute shell commands with real-time output and timing?

```python
from pyutilkit.subprocess import run_command

result = run_command(["git", "status"])
print(f"Exit code: {result.returncode}")
print(f"Duration: {result.elapsed}")
```

→ See [Subprocess Guide](subprocess.md) for advanced usage

### 🔧 Singleton Pattern

Need a single instance of a configuration or service class?

```python
from pyutilkit.classes import Singleton

class AppConfig(metaclass=Singleton):
    def __init__(self):
        self.settings = load_config()

config1 = AppConfig()
config2 = AppConfig()
assert config1 is config2  # Same instance
```

→ See [Classes Guide](classes.md) for use cases

## Next Steps

- Browse individual module guides for detailed examples
- Check out the [Installation Guide](../installation.md) for setup instructions
- Review the [README](../README.md) for an overview of the project
- Explore the [Changelog](../CHANGELOG.md) to see what's new

## Need Help?

- **Issues**: Report bugs or request features on [GitHub Issues](https://github.com/spapanik/pyutilkit/issues)
- **Documentation**: Find a problem with the docs? Let us know!
- **Questions**: Check existing issues or create a new one

Happy coding! 🎉
