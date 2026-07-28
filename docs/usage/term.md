# Terminal Module

The `term` module provides powerful terminal formatting capabilities with ANSI/SGR codes, smart TTY detection, and convenient output utilities. It makes it easy to create colorful, formatted command-line interfaces that work correctly in both interactive terminals and piped output.

## Overview

Terminal formatting can be complex due to:

- Different terminal capabilities
- Piped vs interactive output
- Cross-platform compatibility
- Complex ANSI escape sequences

The `term` module simplifies this by providing:

- Easy-to-use color and style constants
- TTY-aware `.print()` methods that strip colors outside a terminal
- Smart printing to stdout/stderr
- Header formatting with automatic centering
- Environment variable overrides for forcing colors

## Basic Usage

### Creating Styled Strings

```python
from pyutilkit.term import SGRString, SGRCodes

# Create a simple styled string
message = SGRString("Hello, World!", params=[SGRCodes.BOLD])
message.print()  # Writes styled text to stdout on a TTY, plain text when piped

# Multiple styles routed to stderr
error_msg = SGRString(
    "Error: File not found",
    params=[SGRCodes.BOLD, SGRCodes.RED],
    is_error=True,
)
error_msg.print()  # Writes to stderr

# With prefix and suffix
item = SGRString(
    "✓ Success",
    prefix="[APP] ",
    suffix="!",
    params=[SGRCodes.GREEN],
    force_prefix=True,
)
item.print()  # Always writes: [APP] ✓ Success!
```

### Available Styles and Colors

```python
from pyutilkit.term import SGRCodes

# Text styles
styles = [
    SGRCodes.BOLD,
    SGRCodes.ITALIC,
    SGRCodes.UNDERLINE,
    SGRCodes.BLINK,
    SGRCodes.REVERSE,
]

# Foreground colors
foreground_colors = [
    SGRCodes.BLACK,
    SGRCodes.RED,
    SGRCodes.GREEN,
    SGRCodes.YELLOW,
    SGRCodes.BLUE,
    SGRCodes.MAGENTA,
    SGRCodes.CYAN,
    SGRCodes.GREY,
]

# Background colors
background_colors = [
    SGRCodes.BG_BLACK,
    SGRCodes.BG_RED,
    SGRCodes.BG_GREEN,
    SGRCodes.BG_YELLOW,
    SGRCodes.BG_BLUE,
    SGRCodes.BG_MAGENTA,
    SGRCodes.BG_CYAN,
    SGRCodes.BG_GREY,
]

# Bright variants (for better visibility)
bright_colors = [
    SGRCodes.RED_BRIGHT,
    SGRCodes.GREEN_BRIGHT,
    SGRCodes.YELLOW_BRIGHT,
    SGRCodes.BLUE_BRIGHT,
]
```

### String Operations

```python
from pyutilkit.term import SGRString, SGRCodes

# String multiplication preserves formatting
star = SGRString("*", params=[SGRCodes.YELLOW])
stars = star * 5
stars.print()  # Yellow on a TTY, plain when piped

# Length calculation excludes ANSI codes
text = SGRString("Hello", params=[SGRCodes.BOLD, SGRCodes.RED])
print(len(text))  # 5 (not including escape sequences)
```

## Advanced Patterns

### Smart Output with SGROutput

```python
from pyutilkit.term import SGRString, SGROutput, SGRCodes

# Combine multiple styled strings
output = SGROutput(
    [
        SGRString("Status:", params=[SGRCodes.BOLD]),
        SGRString(" OK", params=[SGRCodes.GREEN]),
    ]
)
output.print(sep="")  # Status: OK

# With separator
items = SGROutput(
    [
        SGRString("apple", params=[SGRCodes.RED]),
        SGRString("banana", params=[SGRCodes.YELLOW]),
        SGRString("cherry", params=[SGRCodes.MAGENTA]),
    ]
)
items.print(sep=", ")  # apple, banana, cherry
```

### Error vs Regular Output

```python
from pyutilkit.term import SGRString, SGRCodes

# Regular message (prints to stdout)
info = SGRString("Processing...", params=[SGRCodes.BLUE])
info.print()

# Error message (prints to stderr)
error = SGRString(
    "Failed to connect", params=[SGRCodes.BOLD, SGRCodes.RED], is_error=True
)
error.print()
```

### Styling Prefixes and Suffixes

By default, SGR styling applies only to the main text. Pass `full_color=True`
to include the prefix and suffix inside the styled range:

```python
from pyutilkit.term import SGRString, SGRCodes

status = SGRString(
    "Ready",
    prefix="[STATUS] ",
    suffix="!",
    params=[SGRCodes.GREEN],
    force_prefix=True,
    force_sgr=True,
)
status.print(full_color=True)
# Emits: \x1b[32m[STATUS] Ready!\x1b[0m
```

### Centered Headers

```python
from pyutilkit.term import SGRString, SGRCodes

# Create a centered header
title = SGRString("Application Started", params=[SGRCodes.BOLD, SGRCodes.CYAN])
title.header()  # Centers text based on terminal width

# Custom padding
title.header(padding="=", left_spaces=2, right_spaces=2)
# When terminal size is available, fills its width with "=" around the title
```

### TTY Detection and Overrides

```python
from pyutilkit.term import SGRString, SGRCodes
import os

# By default, colors are stripped when output is not a TTY
regular_message = SGRString("Colored text", params=[SGRCodes.RED])
regular_message.print()  # Colors on a TTY, plain when piped

# Set overrides before constructing the affected object
os.environ["PY_UTIL_FORCE_SGR"] = "yes"
forced_message = SGRString("Colored text", params=[SGRCodes.RED])
forced_message.print()  # Includes colors even when piped

# Force the prefix and suffix even when piped
os.environ["PY_UTIL_FORCE_PREFIX"] = "TRUE"
tagged = SGRString("msg", prefix="[TAG] ", params=[SGRCodes.BOLD])
tagged.print()  # Always includes [TAG] prefix
```

Environment overrides are read when each `SGRString` is constructed; changing
an environment variable does not alter an existing instance. Accepted truthy
values are `1`, `true`, and `yes`, case-insensitively. An explicit
`force_sgr` or `force_prefix` argument takes precedence over the corresponding
environment variable in both directions: `True` enables the output and `False`
disables it. Omit the argument to inherit the environment setting.

## Real-World Examples

### CLI Progress Indicator

```python
from pyutilkit.term import SGRString, SGROutput, SGRCodes
import sys
import time


class ProgressBar:
    """Animated progress bar with colored output."""

    def __init__(self, total: int, width: int = 40):
        self.total = total
        self.width = width
        self.current = 0

    def update(self, current: int):
        """Update progress bar."""
        self.current = min(current, self.total)
        percentage = self.current / self.total
        filled = int(self.width * percentage)
        empty = self.width - filled

        # Build progress bar
        bar = SGRString("█" * filled + "░" * empty, params=[SGRCodes.GREEN])

        # Build percentage text
        pct_text = SGRString(f"{percentage * 100:5.1f}%", params=[SGRCodes.BOLD])

        # Keep each styled component separate so TTY filtering still applies
        output = SGROutput(["\r[", bar, "] ", pct_text])
        output.print(end="")
        sys.stdout.flush()

    def complete(self):
        """Mark progress as complete."""
        self.update(self.total)
        done = SGRString(" ✓ Done", params=[SGRCodes.GREEN, SGRCodes.BOLD])
        done.print()


# Example usage
progress = ProgressBar(100)
for i in range(101):
    progress.update(i)
    time.sleep(0.05)
progress.complete()
```

### TTY-Aware Log Handler

```python
from pyutilkit.term import SGRString, SGROutput, SGRCodes
from datetime import datetime
import logging


class ColorHandler(logging.Handler):
    """Logging handler with TTY-aware colored output."""

    LEVEL_COLORS = {
        logging.DEBUG: SGRCodes.BLUE,
        logging.INFO: SGRCodes.GREEN,
        logging.WARNING: SGRCodes.YELLOW,
        logging.ERROR: SGRCodes.RED,
        logging.CRITICAL: SGRCodes.RED_BRIGHT,
    }

    def emit(self, record: logging.LogRecord) -> None:
        """Write one colored log record to stderr."""
        color = self.LEVEL_COLORS.get(record.levelno, SGRCodes.GREY)
        timestamp = datetime.fromtimestamp(record.created)
        ts_str = SGRString(timestamp.strftime("%H:%M:%S"), params=[SGRCodes.GREY])
        level_str = SGRString(record.levelname.ljust(8), params=[color, SGRCodes.BOLD])
        msg_str = SGRString(record.getMessage(), params=[])

        output = SGROutput([ts_str, level_str, msg_str], is_error=True)
        output.print(sep=" ")


# Configure logger
logger = logging.getLogger("color-example")
logger.handlers.clear()
logger.addHandler(ColorHandler())
logger.setLevel(logging.DEBUG)
logger.propagate = False

# Usage
logger.debug("Debug message")
logger.info("Info message")
logger.warning("Warning message")
logger.error("Error message")
```

### Table Formatter

```python
from pyutilkit.term import SGRString, SGROutput, SGRCodes
from typing import Any


class TableFormatter:
    """Format data as aligned tables with optional colors."""

    def __init__(self, headers: list[str]):
        self.headers = headers
        self.rows: list[list[Any]] = []
        self.col_widths = [len(h) for h in headers]

    def add_row(self, row: list[Any]):
        """Add a row to the table."""
        self.rows.append(row)
        # Update column widths
        for i, cell in enumerate(row):
            if i < len(self.col_widths):
                self.col_widths[i] = max(self.col_widths[i], len(str(cell)))

    def print(self) -> None:
        """Print the table with TTY-aware colors."""
        # Header row
        header_cells = []
        for i, header in enumerate(self.headers):
            cell = SGRString(
                header.ljust(self.col_widths[i]), params=[SGRCodes.BOLD, SGRCodes.CYAN]
            )
            header_cells.append(cell)

        header_output = SGROutput(header_cells)
        header_output.print(sep=" │ ")

        # Separator
        separator = "─" * (sum(self.col_widths) + 3 * (len(self.col_widths) - 1))
        SGRString(separator, params=[SGRCodes.GREY]).print()

        # Data rows
        for row in self.rows:
            cells = []
            for i, value in enumerate(row):
                if i < len(self.col_widths):
                    cell = SGRString(str(value).ljust(self.col_widths[i]), params=[])
                    cells.append(cell)

            row_output = SGROutput(cells)
            row_output.print(sep=" │ ")


# Example usage
table = TableFormatter(["Name", "Age", "City"])
table.add_row(["Alice", 30, "New York"])
table.add_row(["Bob", 25, "London"])
table.add_row(["Charlie", 35, "Tokyo"])

table.print()
# Output:
# Name    │ Age │ City
# ────────────────────────
# Alice   │ 30  │ New York
# Bob     │ 25  │ London
# Charlie │ 35  │ Tokyo
```

### Interactive Menu System

```python
from collections.abc import Callable

from pyutilkit.term import SGRString, SGROutput, SGRCodes


class Menu:
    """Interactive terminal menu with colored options."""

    def __init__(self, title: str):
        self.title = title
        self.options: list[tuple[str, Callable[[], None]]] = []

    def add_option(self, label: str, action: Callable[[], None]):
        """Add menu option."""
        self.options.append((label, action))

    def display(self):
        """Display menu and handle user input."""
        while True:
            # Clear screen (optional)
            print("\n" * 2)

            # Display title
            title = SGRString(self.title, params=[SGRCodes.BOLD, SGRCodes.CYAN])
            title.header(padding="═")

            print()

            # Display options
            for i, (label, _) in enumerate(self.options, 1):
                num = SGRString(f"{i}.", params=[SGRCodes.BOLD, SGRCodes.YELLOW])
                text = SGRString(label, params=[])
                output = SGROutput([num, text])
                output.print(sep=" ")

            print()

            # Exit option
            exit_num = SGRString("0.", params=[SGRCodes.BOLD, SGRCodes.RED])
            exit_text = SGRString("Exit", params=[SGRCodes.RED])
            exit_output = SGROutput([exit_num, exit_text])
            exit_output.print(sep=" ")

            # Get user input
            try:
                choice = input("\nSelect option: ").strip()

                if choice == "0":
                    print("\nGoodbye!")
                    break

                idx = int(choice) - 1
                if 0 <= idx < len(self.options):
                    _, action = self.options[idx]
                    action()
                else:
                    error = SGRString(
                        "Invalid option. Try again.", params=[SGRCodes.RED]
                    )
                    error.print()

            except ValueError:
                error = SGRString("Please enter a number.", params=[SGRCodes.RED])
                error.print()
            except KeyboardInterrupt:
                print("\n\nGoodbye!")
                break


# Example usage
def show_info():
    info = SGRString("This is the info page", params=[SGRCodes.GREEN])
    info.header()
    input("\nPress Enter to continue...")


def show_settings():
    settings = SGRString("Settings panel", params=[SGRCodes.YELLOW])
    settings.header()
    input("\nPress Enter to continue...")


menu = Menu("Main Menu")
menu.add_option("Show Information", show_info)
menu.add_option("Open Settings", show_settings)
menu.display()
```

### Status Dashboard

```python
from pyutilkit.term import SGRString, SGRCodes, SGROutput


class StatusDashboard:
    """Display system status dashboard."""

    @staticmethod
    def status_indicator(is_ok: bool) -> SGRString:
        """Create status indicator."""
        if is_ok:
            return SGRString("●", params=[SGRCodes.GREEN])
        else:
            return SGRString("●", params=[SGRCodes.RED])

    @staticmethod
    def label(text: str) -> SGRString:
        """Create label."""
        return SGRString(text, params=[SGRCodes.BOLD])

    def display(self):
        """Display dashboard."""
        # Title
        title = SGRString(
            "System Status Dashboard", params=[SGRCodes.BOLD, SGRCodes.CYAN]
        )
        title.header(padding="═")
        print()

        # Services
        services = [
            ("Web Server", True),
            ("Database", True),
            ("Cache", False),
            ("Queue", True),
        ]

        for name, is_running in services:
            indicator = self.status_indicator(is_running)
            label = self.label(name.ljust(15))
            status = SGRString(
                "Running" if is_running else "Stopped",
                params=[SGRCodes.GREEN if is_running else SGRCodes.RED],
            )

            output = SGROutput([indicator, label, status])
            output.print(sep=" ")

        print()

        # Metrics
        metrics_label = SGRString("Metrics:", params=[SGRCodes.BOLD, SGRCodes.YELLOW])
        metrics_label.print()

        cpu = SGRString("CPU: 45%", params=[])
        mem = SGRString("Memory: 2.3GB/8GB", params=[])
        disk = SGRString("Disk: 67%", params=[])

        metrics = SGROutput([cpu, mem, disk])
        metrics.print(sep="  ")


# Example usage
dashboard = StatusDashboard()
dashboard.display()
```

## Common Pitfalls

!!! warning "TTY Detection"

    `SGRString.print()` and `SGROutput.print()` strip ANSI codes when output is not attached to a TTY. Converting an `SGRString` with `str()` always retains its codes. Set `PY_UTIL_FORCE_SGR=1` before construction when piped output must retain styling.

!!! warning "Windows Compatibility"

    Older Windows terminals may not support ANSI codes. Modern Windows 10+ terminals do support them. Consider using libraries like `colorama` for broader Windows compatibility if needed.

!!! tip "Use Bright Colors for Better Visibility"

    Standard colors can be hard to read on some terminals. Use bright variants (`RED_BRIGHT`, `GREEN_BRIGHT`, etc.) for better visibility.

!!! tip "Test with Piped Output"

    Always test your CLI tools with piped output (`command | cat`) to ensure they work correctly when colors are stripped.
