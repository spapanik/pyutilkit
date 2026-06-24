# pyutilkit: python's missing batteries

[![build][build_badge]][build_url]
[![lint][lint_badge]][lint_url]
[![tests][tests_badge]][tests_url]
[![license][licence_badge]][licence_url]
[![codecov][codecov_badge]][codecov_url]
[![readthedocs][readthedocs_badge]][readthedocs_url]
[![pypi][pypi_badge]][pypi_url]
[![downloads][pepy_badge]][pepy_url]
[![build automation: yam][yam_badge]][yam_url]
[![Lint: ruff][ruff_badge]][ruff_url]

Python has long maintained the philosophy of "batteries included", providing users with a rich
standard library that avoids the need for third-party tools for most tasks. Some packages are so
common they have achieved similar status to the standard library. Yet, certain utilities are
reimplemented across countless projects. This lightweight library, with minimal dependencies,
aims to eliminate that repetition.

## Quick Start

Install pyutilkit:

```bash
pip install pyutilkit
```

Or with uv (recommended for speed):

```bash
uv pip install pyutilkit
```

Basic usage example:

```python
from pyutilkit.date_utils import now
from pyutilkit.timing import Stopwatch
from pyutilkit.term import SGRString, SGRCodes

# Get current time in any timezone
from zoneinfo import ZoneInfo
tokyo_time = now(ZoneInfo("Asia/Tokyo"))
print(f"Current time in Tokyo: {tokyo_time}")

# Measure execution time
stopwatch = Stopwatch()
with stopwatch:
    # Your code here
    result = sum(range(1000000))
print(f"Computation took: {stopwatch.elapsed}")

# Colorful terminal output
success = SGRString("✓ Task completed", params=[SGRCodes.GREEN, SGRCodes.BOLD])
success.print()
```

## Key Features

- **🕐 Timezone Utilities**: Robust datetime handling with cross-platform timezone support, ISO parsing (including Zulu timezone), and seamless timezone conversion
- **⏱️ High-Precision Timing**: Nanosecond-precision timing with human-readable formatting, lap tracking, and stopwatch functionality
- **🎨 Terminal Formatting**: ANSI color codes with smart TTY detection, automatic style stripping for piped output, and convenient header formatting
- **🛡️ Error Handling**: Elegant exception handling decorator that logs errors and returns defaults instead of raising exceptions
- **📁 File Utilities**: Efficient SHA-256 file hashing with buffered reading for large files
- **🚀 Subprocess Enhancement**: Run shell commands with real-time output streaming, automatic timing, and structured results
- **🔧 Design Patterns**: Thread-safe Singleton metaclass implementation
- **✨ Zero Dependencies**: Pure Python using only standard library (except optional tzdata on Windows)
- **🧪 Fully Tested**: 100% test coverage with comprehensive type annotations

## Documentation

- **[Installation Guide](installation.md)** - Setup instructions and requirements
- **[Usage Guide](usage/index.md)** - Comprehensive examples and tutorials for all modules
  - [Classes](usage/classes.md) - Singleton pattern implementation
  - [Date Utilities](usage/date_utils.md) - Timezone-aware datetime operations
  - [File Utilities](usage/files.md) - Exception handling and file hashing
  - [Subprocess](usage/subprocess.md) - Enhanced command execution
  - [Terminal](usage/term.md) - Terminal formatting and colors
  - [Timing](usage/timing.md) - Performance measurement and benchmarking
- **[Changelog](CHANGELOG.md)** - Version history and changes
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community guidelines

## Requirements

- Python 3.10 or higher
- No external dependencies (tzdata is automatically installed on Windows)

## Links

- [Full Documentation](https://pyutilkit.readthedocs.io/en/stable/)
- [PyPI Package](https://pypi.org/project/pyutilkit)
- [GitHub Repository](https://github.com/spapanik/pyutilkit)
- [Changelog](CHANGELOG.md)
- [Report Issues](https://github.com/spapanik/pyutilkit/issues)

[build_badge]: https://github.com/spapanik/pyutilkit/actions/workflows/build.yml/badge.svg
[build_url]: https://github.com/spapanik/pyutilkit/actions/workflows/build.yml
[lint_badge]: https://github.com/spapanik/pyutilkit/actions/workflows/lint.yml/badge.svg
[lint_url]: https://github.com/spapanik/pyutilkit/actions/workflows/lint.yml
[tests_badge]: https://github.com/spapanik/pyutilkit/actions/workflows/tests.yml/badge.svg
[tests_url]: https://github.com/spapanik/pyutilkit/actions/workflows/tests.yml
[licence_badge]: https://img.shields.io/pypi/l/pyutilkit
[licence_url]: https://pyutilkit.readthedocs.io/en/stable/LICENSE/
[codecov_badge]: https://codecov.io/github/spapanik/pyutilkit/graph/badge.svg?token=Q20F84BW72
[codecov_url]: https://codecov.io/github/spapanik/pyutilkit
[readthedocs_badge]: https://readthedocs.org/projects/pyutilkit/badge/?version=latest
[readthedocs_url]: https://pyutilkit.readthedocs.io/en/latest/
[pypi_badge]: https://img.shields.io/pypi/v/pyutilkit
[pypi_url]: https://pypi.org/project/pyutilkit
[pepy_badge]: https://pepy.tech/badge/pyutilkit
[pepy_url]: https://pepy.tech/project/pyutilkit
[yam_badge]: https://img.shields.io/badge/build%20automation-yamk-success
[yam_url]: https://github.com/spapanik/yamk
[ruff_badge]: https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/charliermarsh/ruff/main/assets/badge/v1.json
[ruff_url]: https://github.com/charliermarsh/ruff
[Documentation]: https://pyutilkit.readthedocs.io/en/stable/
[Changelog]: https://pyutilkit.readthedocs.io/en/stable/CHANGELOG/
