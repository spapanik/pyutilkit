# Installation

This guide covers different ways to install pyutilkit and verify your setup.

## Prerequisites

- **Python 3.10 or higher** - pyutilkit requires modern Python features
- **pip** or **[uv]** (recommended) for package installation

Check your Python version:

```bash
python --version
# or
python3 --version
```

If you need to upgrade Python, visit [python.org](https://www.python.org/downloads/)

## Quick Installation

### Using uv (Recommended)

[uv] is an extremely fast Python package installer and resolver, written in Rust.
It's significantly faster than pip and provides better dependency resolution.

Install uv first:

```bash
# macOS
brew install uv

# Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Then install pyutilkit:

```bash
uv pip install pyutilkit
```

### Using pip

If you prefer traditional pip:

```bash
pip install pyutilkit
```

Or with Python 3 explicitly:

```bash
python3 -m pip install pyutilkit
```

## Installation in Virtual Environments

It's recommended to install pyutilkit in a virtual environment to avoid conflicts
with system packages.

### Using venv (Standard Library)

```bash
# Create virtual environment
python3 -m venv myproject-env

# Activate it
# On macOS/Linux:
source myproject-env/bin/activate
# On Windows:
myproject-env\Scripts\activate

# Install pyutilkit
pip install pyutilkit

# Verify installation
python -c "import pyutilkit; print(pyutilkit.__version__)"
```

### Using uv venv

```bash
# Create virtual environment with uv
uv venv myproject-env

# Activate it
source myproject-env/bin/activate  # macOS/Linux
# or
myproject-env\Scripts\activate     # Windows

# Install pyutilkit (much faster than pip!)
uv pip install pyutilkit

# Verify installation
python -c "import pyutilkit; print(pyutilkit.__version__)"
```

## Project Integration

### Using a PEP 621 compliant build backend

[PEP 621] is the standard way to store dependencies in a `pyproject.toml` file.
Add pyutilkit to your project dependencies:

```toml
[project]
dependencies = [
    "pyutilkit~=0.11",
    # ... other dependencies
]
```

Then install with:

```bash
# With pip
pip install -e .

# With uv (faster)
uv sync
```

### Using requirements.txt

For simpler projects, add to `requirements.txt`:

```
pyutilkit>=0.11.0,<0.12.0
```

Then install:

```bash
pip install -r requirements.txt
```

## Verification

After installation, verify that pyutilkit is working correctly:

```python
python3 << 'EOF'
import pyutilkit
from pyutilkit.date_utils import now
from pyutilkit.timing import Stopwatch
from pyutilkit.term import SGRString, SGRCodes

# Check version
print(f"pyutilkit version: {pyutilkit.__version__}")

# Test timezone utilities
from zoneinfo import ZoneInfo
tokyo_time = now(ZoneInfo("Asia/Tokyo"))
print(f"Current time in Tokyo: {tokyo_time}")

# Test timing
stopwatch = Stopwatch()
with stopwatch:
    total = sum(range(1000))
print(f"Sum calculation took: {stopwatch.elapsed}")

# Test terminal formatting
success = SGRString("✓ Installation verified!", params=[SGRCodes.GREEN, SGRCodes.BOLD])
success.print()

print("\nAll tests passed! pyutilkit is ready to use.")
EOF
```

Expected output:

```
pyutilkit version: 0.11.0
Current time in Tokyo: 2024-01-15 19:30:00+09:00
Sum calculation took: 45.2µs
✓ Installation verified!

All tests passed! pyutilkit is ready to use.
```

## Platform-Specific Notes

### Windows

On Windows, the `tzdata` package is automatically installed as a dependency to provide
timezone information. This is handled automatically by pip/uv.

### macOS

No special configuration needed. All timezone data is included in macOS.

### Linux

Most modern Linux distributions include timezone data. If you encounter timezone issues,
install the tzdata package for your distribution:

```bash
# Ubuntu/Debian
sudo apt-get install tzdata

# Fedora/RHEL
sudo dnf install tzdata

# Arch Linux
sudo pacman -S tzdata
```

## Troubleshooting

### Import Error

If you get `ModuleNotFoundError: No module named 'pyutilkit'`:

1. Verify pyutilkit is installed:
   ```bash
   pip list | grep pyutilkit
   ```

2. Check you're using the correct Python:
   ```bash
   which python  # macOS/Linux
   where python  # Windows
   ```

3. Ensure your virtual environment is activated (if using one)

### Python Version Error

If you see errors about Python version:

```bash
# Check your Python version
python3 --version

# If it's below 3.10, install a newer version
# Visit https://www.python.org/downloads/
```

### Timezone Issues

If timezone operations fail:

```python
# Test timezone support
from pyutilkit.date_utils import get_timezones
print(f"Available timezones: {len(get_timezones())}")

# Should print 400+ timezones
```

If you see very few timezones, install/update tzdata:

```bash
pip install --upgrade tzdata
```

## Next Steps

Now that pyutilkit is installed, check out:

- **[Usage Guide](usage/index.md)** - Learn how to use each module with examples
- **[Quick Start](README.md#quick-start)** - See basic usage examples
- **[API Documentation](https://pyutilkit.readthedocs.io/)** - Detailed API reference

## Need Help?

- **Documentation**: Browse the [full documentation](https://pyutilkit.readthedocs.io/)
- **Issues**: Report problems on [GitHub Issues](https://github.com/spapanik/pyutilkit/issues)
- **Questions**: Check existing issues or create a new discussion

[uv]: https://github.com/astral-sh/uv
[PEP 621]: https://peps.python.org/pep-0621/
