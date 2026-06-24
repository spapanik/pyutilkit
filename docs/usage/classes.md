# Classes Module

The `classes` module provides design pattern implementations to simplify common object-oriented programming patterns in Python.

## Singleton Pattern

The `Singleton` metaclass ensures that a class has only one instance throughout the application lifecycle, providing a global point of access to that instance.

### When to Use Singletons

Singletons are useful when you need exactly one instance of a class to coordinate actions across your system:

- Configuration managers
- Database connection pools
- Logging services
- Cache managers
- Application state managers

### Basic Usage

```python
from pyutilkit.classes import Singleton


class AppConfig(metaclass=Singleton):
    def __init__(self):
        self.settings = {}
        self._load_config()

    def _load_config(self):
        self.settings['debug'] = False
        self.settings['database_url'] = 'postgresql://localhost/mydb'

    def get(self, key):
        return self.settings.get(key)


# Both calls return the same instance
config1 = AppConfig()
config2 = AppConfig()

assert config1 is config2  # True - same instance
```

### Thread Safety

The `Singleton` implementation is thread-safe using double-checked locking:

```python
import threading
from pyutilkit.classes import Singleton


class ThreadSafeCounter(metaclass=Singleton):
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.count += 1
            return self.count


# Safe to use from multiple threads
counter = ThreadSafeCounter()
```

### Real-World Examples

#### Configuration Manager

```python
from pyutilkit.classes import Singleton
import os


class EnvironmentConfig(metaclass=Singleton):
    """Centralized environment configuration."""

    def __init__(self):
        self.debug = os.getenv('DEBUG', 'false').lower() == 'true'
        self.database_url = os.getenv('DATABASE_URL')
        self.api_key = os.getenv('API_KEY')
        self.max_retries = int(os.getenv('MAX_RETRIES', '3'))

    def is_production(self):
        return not self.debug


# Access from anywhere in your application
config = EnvironmentConfig()
if config.is_production():
    print("Running in production mode")
```

#### Database Connection Pool

```python
from pyutilkit.classes import Singleton


class DatabasePool(metaclass=Singleton):
    """Simple database connection pool."""

    def __init__(self):
        self._connections = []
        self._initialize_pool()

    def _initialize_pool(self, size=5):
        """Create initial pool of connections."""
        for i in range(size):
            conn = self._create_connection()
            self._connections.append(conn)

    def _create_connection(self):
        """Simulate creating a database connection."""
        return {"id": id(self), "status": "connected"}

    def get_connection(self):
        """Get a connection from the pool."""
        if self._connections:
            return self._connections.pop()
        raise RuntimeError("No available connections")

    def release_connection(self, conn):
        """Return a connection to the pool."""
        self._connections.append(conn)


# Use the same pool everywhere
pool = DatabasePool()
conn = pool.get_connection()
# ... use connection ...
pool.release_connection(conn)
```

### Common Pitfalls

!!! warning "Testing Challenges"
    Singletons can make testing difficult because state persists between tests. Consider resetting the singleton instance between tests:

    ```python
    # In your test teardown
    def tearDown(self):
        MySingleton.instance = None
    ```

!!! warning "Hidden Dependencies"
    Singletons create implicit dependencies that can make code harder to understand and maintain. Use dependency injection when possible for better testability.

!!! tip "When NOT to Use Singletons"
    - When you might need multiple instances in the future
    - For simple utility functions (use modules instead)
    - When state management becomes complex (consider a proper state management solution)

### API Reference

::: pyutilkit.classes.Singleton
    handler: python
    options:
      show_root_heading: true
      show_source: false
      members:
        - __init__
        - __call__
