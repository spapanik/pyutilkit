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
- Automatic TTY detection (strips colors when not in a terminal)
- Smart printing to stdout/stderr
- Header formatting with automatic centering
- Environment variable overrides for forcing colors

## Basic Usage

### Creating Styled Strings

```python
from pyutilkit.term import SGRString, SGRCodes

# Create a simple styled string
message = SGRString("Hello, World!", params=[SGRCodes.BOLD])
print(message)  # Bold text in terminal, plain text when piped

# Multiple styles
error_msg = SGRString(
    "Error: File not found",
    params=[SGRCodes.BOLD, SGRCodes.RED]
)
error_msg.print()  # Prints to stderr (if is_error=True) or stdout

# With prefix and suffix
item = SGRString(
    "✓ Success",
    prefix="[APP] ",
    suffix="\n",
    params=[SGRCodes.GREEN]
)
item.print()  # [APP] ✓ Success
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
print(stars)  # ***** (all yellow)

# Length calculation excludes ANSI codes
text = SGRString("Hello", params=[SGRCodes.BOLD, SGRCodes.RED])
print(len(text))  # 5 (not including escape sequences)
```

## Advanced Patterns

### Smart Output with SGROutput

```python
from pyutilkit.term import SGRString, SGROutput, SGRCodes

# Combine multiple styled strings
output = SGROutput([
    SGRString("Status:", params=[SGRCodes.BOLD]),
    SGRString(" OK", params=[SGRCodes.GREEN]),
])
output.print(sep="")  # Status: OK

# With separator
items = SGROutput([
    SGRString("apple", params=[SGRCodes.RED]),
    SGRString("banana", params=[SGRCodes.YELLOW]),
    SGRString("cherry", params=[SGRCodes.MAGENTA]),
])
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
    "Failed to connect",
    params=[SGRCodes.BOLD, SGRCodes.RED],
    is_error=True
)
error.print()
```

### Centered Headers

```python
from pyutilkit.term import SGRString, SGRCodes

# Create a centered header
title = SGRString(
    "Application Started",
    params=[SGRCodes.BOLD, SGRCodes.CYAN]
)
title.header()  # Centers text based on terminal width

# Custom padding
title.header(padding="=", left_spaces=2, right_spaces=2)
# == Application Started ==
```

### TTY Detection and Overrides

```python
from pyutilkit.term import SGRString, SGRCodes
import os

# By default, colors are stripped when output is not a TTY
message = SGRString("Colored text", params=[SGRCodes.RED])
message.print()  # Colors if TTY, plain if piped

# Force colors even when piped
os.environ["PY_UTIL_FORCE_SGR"] = "1"
message.print()  # Always includes colors

# Force prefix/suffix even when piped
os.environ["PY_UTIL_FORCE_PREFIX"] = "1"
tagged = SGRString("msg", prefix="[TAG] ", params=[SGRCodes.BOLD])
tagged.print()  # Always includes [TAG] prefix
```

## Real-World Examples

### CLI Progress Indicator

```python
from pyutilkit.term import SGRString, SGRCodes
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
        bar = SGRString(
            "█" * filled + "░" * empty,
            params=[SGRCodes.GREEN]
        )

        # Build percentage text
        pct_text = SGRString(
            f"{percentage * 100:5.1f}%",
            params=[SGRCodes.BOLD]
        )

        # Combine and print
        output = SGRString(
            f"\r[{bar}] {pct_text}",
            params=[]
        )
        output.print(end="")
        sys.stdout.flush()

    def complete(self):
        """Mark progress as complete."""
        self.update(self.total)
        done = SGRString(" ✓ Done\n", params=[SGRCodes.GREEN, SGRCodes.BOLD])
        done.print()


# Example usage
progress = ProgressBar(100)
for i in range(101):
    progress.update(i)
    time.sleep(0.05)
progress.complete()
```

### Log Formatter

```python
from pyutilkit.term import SGRString, SGROutput, SGRCodes
from datetime import datetime
import logging


class ColorFormatter(logging.Formatter):
    """Colored log formatter for console output."""

    LEVEL_COLORS = {
        logging.DEBUG: SGRCodes.BLUE,
        logging.INFO: SGRCodes.GREEN,
        logging.WARNING: SGRCodes.YELLOW,
        logging.ERROR: SGRCodes.RED,
        logging.CRITICAL: SGRCodes.RED_BRIGHT,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format log record with colors."""
        # Get color for level
        color = self.LEVEL_COLORS.get(record.levelno, SGRCodes.GREY)

        # Format timestamp
        timestamp = datetime.fromtimestamp(record.created)
        ts_str = SGRString(
            timestamp.strftime("%H:%M:%S"),
            params=[SGRCodes.GREY]
        )

        # Format level
        level_str = SGRString(
            record.levelname.ljust(8),
            params=[color, SGRCodes.BOLD]
        )

        # Format message
        msg_str = SGRString(
            record.getMessage(),
            params=[]
        )

        # Combine
        output = SGROutput([ts_str, level_str, msg_str])
        return str(output)


# Configure logger
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(ColorFormatter())
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

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

    def render(self) -> str:
        """Render table as formatted string."""
        lines = []

        # Header row
        header_cells = []
        for i, header in enumerate(self.headers):
            cell = SGRString(
                header.ljust(self.col_widths[i]),
                params=[SGRCodes.BOLD, SGRCodes.CYAN]
            )
            header_cells.append(cell)

        header_output = SGROutput(header_cells)
        lines.append(str(header_output).replace(" ", " │ "))

        # Separator
        separator = "─" * (sum(self.col_widths) + 3 * (len(self.col_widths) - 1))
        lines.append(SGRString(separator, params=[SGRCodes.GREY]).__str__())

        # Data rows
        for row in self.rows:
            cells = []
            for i, value in enumerate(row):
                if i < len(self.col_widths):
                    cell = SGRString(
                        str(value).ljust(self.col_widths[i]),
                        params=[]
                    )
                    cells.append(cell)

            row_output = SGROutput(cells)
            lines.append(str(row_output).replace(" ", " │ "))

        return "\n".join(lines)


# Example usage
table = TableFormatter(["Name", "Age", "City"])
table.add_row(["Alice", 30, "New York"])
table.add_row(["Bob", 25, "London"])
table.add_row(["Charlie", 35, "Tokyo"])

print(table.render())
# Output:
# Name    │ Age │ City
# ───────────────────────
# Alice   │ 30  │ New York
# Bob     │ 25  │ London
# Charlie │ 35  │ Tokyo
```

### Interactive Menu System

```python
from pyutilkit.term import SGRString, SGRCodes
import sys


class Menu:
    """Interactive terminal menu with colored options."""

    def __init__(self, title: str):
        self.title = title
        self.options: list[tuple[str, callable]] = []

    def add_option(self, label: str, action: callable):
        """Add menu option."""
        self.options.append((label, action))

    def display(self):
        """Display menu and handle user input."""
        while True:
            # Clear screen (optional)
            print("\n" * 2)

            # Display title
            title = SGRString(
                self.title,
                params=[SGRCodes.BOLD, SGRCodes.CYAN]
            )
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
                        "Invalid option. Try again.",
                        params=[SGRCodes.RED]
                    )
                    error.print()

            except ValueError:
                error = SGRString(
                    "Please enter a number.",
                    params=[SGRCodes.RED]
                )
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
import os


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
            "System Status Dashboard",
            params=[SGRCodes.BOLD, SGRCodes.CYAN]
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
                params=[SGRCodes.GREEN if is_running else SGRCodes.RED]
            )

            output = SGROutput([indicator, label, status])
            output.print(sep=" ")

        print()

        # Metrics
        metrics_label = SGRString(
            "Metrics:",
            params=[SGRCodes.BOLD, SGRCodes.YELLOW]
        )
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
    When piping output to a file or another command, ANSI codes are automatically stripped. This is usually desired behavior, but you can override it with `PY_UTIL_FORCE_SGR=1`.

!!! warning "Windows Compatibility"
    Older Windows terminals may not support ANSI codes. Modern Windows 10+ terminals do support them. Consider using libraries like `colorama` for broader Windows compatibility if needed.

!!! tip "Use Bright Colors for Better Visibility"
    Standard colors can be hard to read on some terminals. Use bright variants (`RED_BRIGHT`, `GREEN_BRIGHT`, etc.) for better visibility.

!!! tip "Test with Piped Output"
    Always test your CLI tools with piped output (`command | cat`) to ensure they work correctly when colors are stripped.

## API Reference

::: pyutilkit.term
    handler: python
    options:
      show_root_heading: true
      show_source: false
      members:
        - SGRCodes
        - SGRString
        - SGROutput
