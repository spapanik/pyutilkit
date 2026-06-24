# Files Module

The `files` module provides utility functions for file operations and robust exception handling. It includes a powerful decorator for graceful error handling and efficient file hashing for integrity verification.

## Exception Handling Decorator

The `handle_exceptions` decorator provides a clean way to handle exceptions in functions without cluttering your code with try-except blocks. It logs errors and returns a default value instead of raising exceptions.

### Basic Usage

```python
from pyutilkit.files import handle_exceptions


@handle_exceptions()
def risky_operation(x: int) -> float:
    """This function might fail, but won't raise exceptions."""
    return 100 / x


# Normal case
result = risky_operation(10)
print(result)  # 10.0

# Exception case - returns None (default)
result = risky_operation(0)
print(result)  # None
# Logs: Function `risky_operation` threw `ZeroDivisionError` when called with args=(0,) and kwargs={}
```

### Custom Default Values

```python
from pyutilkit.files import handle_exceptions


@handle_exceptions(default=0.0)
def safe_divide(a: int, b: int) -> float:
    """Returns 0.0 on division by zero."""
    return a / b


print(safe_divide(10, 2))   # 5.0
print(safe_divide(10, 0))   # 0.0 (default value)
```

### Selective Exception Handling

```python
from pyutilkit.files import handle_exceptions


@handle_exceptions(exceptions=(ValueError, TypeError), default=-1)
def parse_and_double(value: str) -> int:
    """Parse string to int and double it."""
    return int(value) * 2


print(parse_and_double("5"))     # 10
print(parse_and_double("abc"))   # -1 (ValueError caught)
print(parse_and_double(None))    # -1 (TypeError caught)

# This will still raise an exception (not in the handled list)
try:
    parse_and_double(1/0)  # ZeroDivisionError
except ZeroDivisionError:
    print("ZeroDivisionError was not caught")
```

### Custom Log Levels

```python
from pyutilkit.files import handle_exceptions
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)


@handle_exceptions(default=None, log_level="error")
def critical_operation(data: dict) -> str:
    """Log failures as errors."""
    return data['key']


result = critical_operation({})  # Logs as ERROR level
```

## Real-World Examples

### Data Pipeline Error Handling

```python
from pyutilkit.files import handle_exceptions
from typing import Any


class DataProcessor:
    """Process data records with graceful error handling."""

    @handle_exceptions(exceptions=(KeyError, ValueError), default=None)
    def extract_field(self, record: dict, field: str) -> Any:
        """Safely extract a field from a record."""
        return record[field]

    @handle_exceptions(exceptions=(TypeError, ValueError), default=0.0)
    def parse_price(self, price_str: str) -> float:
        """Parse price string to float."""
        # Remove currency symbols and commas
        cleaned = price_str.replace('$', '').replace(',', '')
        return float(cleaned)

    @handle_exceptions(exceptions=Exception, default=[])
    def process_records(self, records: list[dict]) -> list[dict]:
        """Process multiple records, skipping failed ones."""
        processed = []
        for record in records:
            try:
                processed_record = {
                    'name': self.extract_field(record, 'name'),
                    'price': self.parse_price(record.get('price', '0')),
                }
                if processed_record['name'] is not None:
                    processed.append(processed_record)
            except Exception:
                continue
        return processed


# Example usage
processor = DataProcessor()
records = [
    {'name': 'Product A', 'price': '$10.99'},
    {'name': 'Product B', 'price': 'invalid'},  # Will use default 0.0
    {'price': '$5.00'},  # Missing name - will be skipped
    {'name': 'Product C', 'price': '$1,234.56'},
]

results = processor.process_records(records)
for result in results:
    print(result)
# Output:
# {'name': 'Product A', 'price': 10.99}
# {'name': 'Product B', 'price': 0.0}
# {'name': 'Product C', 'price': 1234.56}
```

### API Request Handler

```python
from pyutilkit.files import handle_exceptions
import requests


class APIClient:
    """HTTP client with automatic error handling."""

    def __init__(self, base_url: str):
        self.base_url = base_url

    @handle_exceptions(
        exceptions=(requests.RequestException, ConnectionError),
        default=None,
        log_level="warning"
    )
    def get_data(self, endpoint: str) -> dict | None:
        """Fetch data from API endpoint."""
        url = f"{self.base_url}/{endpoint}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()

    @handle_exceptions(exceptions=Exception, default=False)
    def health_check(self) -> bool:
        """Check if API is healthy."""
        url = f"{self.base_url}/health"
        response = requests.get(url, timeout=5)
        return response.status_code == 200


# Example usage
client = APIClient("https://api.example.com")

# Returns None on failure instead of raising exception
data = client.get_data("users/123")
if data is None:
    print("Failed to fetch user data (logged as warning)")
else:
    print(f"User data: {data}")

# Health check returns False on failure
is_healthy = client.health_check()
print(f"API status: {'healthy' if is_healthy else 'unhealthy'}")
```

### File Processing Pipeline

```python
from pyutilkit.files import handle_exceptions
from pathlib import Path
import json


class FileProcessor:
    """Process files with comprehensive error handling."""

    @handle_exceptions(exceptions=(json.JSONDecodeError, IOError), default={})
    def load_json(self, filepath: Path) -> dict:
        """Load JSON file safely."""
        with open(filepath, 'r') as f:
            return json.load(f)

    @handle_exceptions(exceptions=OSError, default=None)
    def read_config(self, config_path: Path) -> dict | None:
        """Read configuration file."""
        if not config_path.exists():
            return None
        return self.load_json(config_path)

    @handle_exceptions(
        exceptions=(KeyError, TypeError, ValueError),
        default="unknown"
    )
    def extract_value(self, data: dict, key: str) -> str:
        """Safely extract value from nested dict."""
        return str(data[key]['value'])


# Example usage
processor = FileProcessor()

# Load config with fallback
config = processor.read_config(Path("config.json"))
if config is None:
    print("Using default configuration")
    config = {"default": True}

# Extract values safely
value = processor.extract_value(config, "database")
print(f"Database: {value}")
```

## File Hashing

The `hash_file` function computes SHA-256 hashes of files efficiently using buffered reading, making it suitable for large files.

### Basic Usage

```python
from pyutilkit.files import hash_file
from pathlib import Path

# Hash a file
file_hash = hash_file(Path("/path/to/file.txt"))
print(file_hash)
# Output: e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855

# Hash with custom buffer size (for very large files)
large_file_hash = hash_file(Path("/path/to/large.iso"), buffer_size=2**20)  # 1MB buffer
```

### Real-World Examples

#### File Integrity Verification

```python
from pyutilkit.files import hash_file
from pathlib import Path


class FileIntegrityChecker:
    """Verify file integrity using SHA-256 hashes."""

    def __init__(self, checksum_file: Path):
        self.checksum_file = checksum_file
        self.known_hashes = self._load_checksums()

    def _load_checksums(self) -> dict[str, str]:
        """Load known file hashes."""
        hashes = {}
        if self.checksum_file.exists():
            with open(self.checksum_file, 'r') as f:
                for line in f:
                    if line.strip():
                        hash_val, filename = line.strip().split('  ', 1)
                        hashes[filename] = hash_val
        return hashes

    def verify_file(self, filepath: Path) -> bool:
        """Verify a file's integrity."""
        current_hash = hash_file(filepath)
        expected_hash = self.known_hashes.get(filepath.name)

        if expected_hash is None:
            print(f"No known hash for {filepath.name}")
            return False

        is_valid = current_hash == expected_hash
        if is_valid:
            print(f"✓ {filepath.name} integrity verified")
        else:
            print(f"✗ {filepath.name} integrity check FAILED")
            print(f"  Expected: {expected_hash}")
            print(f"  Got:      {current_hash}")
        return is_valid

    def update_checksums(self, directory: Path):
        """Update checksums for all files in directory."""
        with open(self.checksum_file, 'w') as f:
            for filepath in directory.glob('*'):
                if filepath.is_file():
                    file_hash = hash_file(filepath)
                    f.write(f"{file_hash}  {filepath.name}\n")
        print(f"Checksums updated in {self.checksum_file}")


# Example usage
checker = FileIntegrityChecker(Path("checksums.sha256"))

# Verify downloaded file
downloaded = Path("downloads/software.tar.gz")
if checker.verify_file(downloaded):
    print("File is safe to use")
else:
    print("WARNING: File may be corrupted or tampered with!")
```

#### Duplicate File Finder

```python
from pyutilkit.files import hash_file
from pathlib import Path
from collections import defaultdict


def find_duplicates(directory: Path) -> dict[str, list[Path]]:
    """Find duplicate files in a directory using SHA-256 hashes.

    Args:
        directory: Directory to scan for duplicates

    Returns:
        Dictionary mapping file hashes to lists of duplicate paths
    """
    hash_to_files = defaultdict(list)

    # Hash all files
    for filepath in directory.rglob('*'):
        if filepath.is_file():
            file_hash = hash_file(filepath)
            hash_to_files[file_hash].append(filepath)

    # Filter to only duplicates
    duplicates = {
        hash_val: files
        for hash_val, files in hash_to_files.items()
        if len(files) > 1
    }

    return duplicates


# Example usage
duplicates = find_duplicates(Path("/path/to/photos"))

for hash_val, files in duplicates.items():
    print(f"\nDuplicate group (hash: {hash_val[:16]}...):")
    for filepath in files:
        size_mb = filepath.stat().st_size / (1024 * 1024)
        print(f"  - {filepath} ({size_mb:.2f} MB)")
    print(f"  Potential space savings: {(len(files) - 1) * files[0].stat().st_size / (1024*1024):.2f} MB")
```

#### Cache Validation

```python
from pyutilkit.files import hash_file
from pathlib import Path
import json


class CacheManager:
    """Manage file-based cache with hash validation."""

    def __init__(self, cache_dir: Path):
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = cache_dir / "cache_metadata.json"
        self.metadata = self._load_metadata()

    def _load_metadata(self) -> dict:
        """Load cache metadata."""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return {}

    def _save_metadata(self):
        """Save cache metadata."""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)

    def get_cached(self, source_file: Path) -> Path | None:
        """Get cached processed file if source hasn't changed."""
        source_hash = hash_file(source_file)
        cache_key = str(source_file)

        if cache_key in self.metadata:
            cached_info = self.metadata[cache_key]
            if cached_info['source_hash'] == source_hash:
                cached_file = self.cache_dir / cached_info['cached_filename']
                if cached_file.exists():
                    print(f"Cache hit for {source_file.name}")
                    return cached_file

        print(f"Cache miss for {source_file.name}")
        return None

    def store_in_cache(self, source_file: Path, processed_file: Path) -> Path:
        """Store processed file in cache."""
        source_hash = hash_file(source_file)
        cache_filename = f"{source_hash}.processed"
        cache_path = self.cache_dir / cache_filename

        # Copy processed file to cache
        import shutil
        shutil.copy2(processed_file, cache_path)

        # Update metadata
        self.metadata[str(source_file)] = {
            'source_hash': source_hash,
            'cached_filename': cache_filename,
            'timestamp': processed_file.stat().st_mtime
        }
        self._save_metadata()

        return cache_path


# Example usage
cache = CacheManager(Path(".cache"))
source = Path("data/input.csv")

# Check cache first
cached_result = cache.get_cached(source)
if cached_result:
    print("Using cached result")
    result = cached_result
else:
    print("Processing file...")
    # ... process file ...
    processed = Path("data/output.csv")
    result = cache.store_in_cache(source, processed)
    print(f"Result cached at {result}")
```

## Common Pitfalls

!!! warning "Silent Failures"
    The `handle_exceptions` decorator can mask bugs by catching all exceptions. Always specify the exact exceptions you expect, and use appropriate log levels to ensure failures are visible during development.

!!! tip "Use Specific Exceptions"
    Instead of catching `Exception`, catch specific exceptions like `ValueError`, `KeyError`, etc. This makes debugging easier and prevents hiding unexpected errors.

!!! warning "Buffer Size Trade-offs"
    For `hash_file`, larger buffer sizes are faster but use more memory. The default (64KB) is good for most cases. Use larger buffers (1MB+) only for very large files (>1GB).

!!! tip "Hash Collisions"
    SHA-256 collisions are extremely unlikely but theoretically possible. For critical security applications, consider additional verification methods beyond just hash comparison.

## API Reference

::: pyutilkit.files
    handler: python
    options:
      show_root_heading: true
      show_source: false
      members:
        - handle_exceptions
        - hash_file
