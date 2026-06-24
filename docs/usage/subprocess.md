# Subprocess Module

The `subprocess` module provides enhanced subprocess execution with real-time output streaming, structured results, and built-in timing. It simplifies running shell commands while capturing their output and measuring performance.

## Overview

Python's standard `subprocess` module is powerful but can be verbose for common tasks. This module provides a cleaner API that:

- Streams stdout/stderr in real-time to the console
- Captures output for programmatic access
- Measures execution time automatically
- Returns structured results with all relevant information

## Basic Usage

### Running Simple Commands

```python
from pyutilkit.subprocess import run_command

# Run a simple command
result = run_command(["echo", "Hello, World!"])

print(result.stdout)      # b"Hello, World!\n"
print(result.returncode)  # 0
print(result.pid)         # 12345 (process ID)
print(result.elapsed)     # Timing object (e.g., "5.2ms")
```

### Commands with Arguments

```python
from pyutilkit.subprocess import run_command

# List files in current directory
result = run_command(["ls", "-la", "/tmp"])

if result.returncode == 0:
    print("Command succeeded")
    print(f"Output:\n{result.stdout.decode()}")
else:
    print(f"Command failed with code {result.returncode}")
    print(f"Error:\n{result.stderr.decode()}")
```

### String Commands

```python
from pyutilkit.subprocess import run_command

# You can also pass commands as strings (uses shell)
result = run_command("echo 'Hello from shell'")
print(result.stdout)  # b"Hello from shell\n"
```

## Advanced Patterns

### Working Directory and Environment

```python
from pyutilkit.subprocess import run_command
from pathlib import Path
import os

# Run command in specific directory
result = run_command(
    ["git", "status"],
    cwd=Path("/path/to/repo")
)

# Run with custom environment variables
custom_env = os.environ.copy()
custom_env["MY_VAR"] = "my_value"
result = run_command(
    ["python", "script.py"],
    env=custom_env
)
```

### Handling Command Failures

```python
from pyutilkit.subprocess import run_command


def run_with_error_handling(command: list[str]) -> dict:
    """Run command and handle errors gracefully."""
    result = run_command(command)

    if result.returncode != 0:
        error_msg = result.stderr.decode().strip()
        raise RuntimeError(
            f"Command failed (exit code {result.returncode}): {error_msg}"
        )

    return {
        'output': result.stdout.decode(),
        'elapsed': result.elapsed,
        'pid': result.pid
    }


# Example usage
try:
    info = run_with_error_handling(["git", "rev-parse", "HEAD"])
    print(f"Current commit: {info['output'].strip()}")
    print(f"Execution time: {info['elapsed']}")
except RuntimeError as e:
    print(f"Error: {e}")
```

### Real-Time Output Streaming

The `run_command` function automatically streams output to the console while capturing it:

```python
from pyutilkit.subprocess import run_command

# Long-running command - you'll see output in real-time
result = run_command(["ping", "-c", "4", "google.com"])

# Output is still captured for later use
print(f"\nCaptured {len(result.stdout)} bytes of stdout")
print(f"Command took {result.elapsed}")
```

## Real-World Examples

### Build Script Runner

```python
from pyutilkit.subprocess import run_command
from pathlib import Path
import sys


class BuildRunner:
    """Automated build script runner with error handling."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def run_step(self, name: str, command: list[str]) -> bool:
        """Run a build step and report results."""
        print(f"\n{'='*60}")
        print(f"Running: {name}")
        print(f"Command: {' '.join(command)}")
        print(f"{'='*60}")

        result = run_command(command, cwd=self.project_dir)

        if result.returncode == 0:
            print(f"✓ {name} completed in {result.elapsed}")
            return True
        else:
            print(f"✗ {name} failed (exit code {result.returncode})")
            if result.stderr:
                print(f"Error output:\n{result.stderr.decode()}")
            return False

    def build(self) -> bool:
        """Run complete build pipeline."""
        steps = [
            ("Install dependencies", ["uv", "sync"]),
            ("Run linter", ["uv", "run", "ruff", "check", "."]),
            ("Run tests", ["uv", "run", "pytest"]),
            ("Build package", ["uv", "build"]),
        ]

        for name, command in steps:
            if not self.run_step(name, command):
                print(f"\nBuild failed at step: {name}")
                return False

        print("\n✓ Build completed successfully!")
        return True


# Example usage
if __name__ == "__main__":
    runner = BuildRunner(Path("."))
    success = runner.build()
    sys.exit(0 if success else 1)
```

### System Monitoring Tool

```python
from pyutilkit.subprocess import run_command
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SystemMetrics:
    """System metrics collected from commands."""
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float


class SystemMonitor:
    """Collect system metrics using shell commands."""

    def collect_metrics(self) -> SystemMetrics:
        """Collect current system metrics."""
        # Get CPU usage
        cpu_result = run_command(["top", "-l", "1", "-n", "0"])
        cpu_line = self._parse_cpu(cpu_result.stdout.decode())

        # Get memory usage
        mem_result = run_command(["free", "-m"])
        mem_info = self._parse_memory(mem_result.stdout.decode())

        # Get disk usage
        disk_result = run_command(["df", "-h", "/"])
        disk_info = self._parse_disk(disk_result.stdout.decode())

        return SystemMetrics(
            timestamp=datetime.now(),
            cpu_usage=cpu_line,
            memory_usage=mem_info,
            disk_usage=disk_info
        )

    def _parse_cpu(self, output: str) -> float:
        """Parse CPU usage from top output."""
        # Simplified parsing - adjust based on your system
        for line in output.split('\n'):
            if 'CPU' in line:
                # Extract CPU percentage (implementation depends on OS)
                return 0.0  # Placeholder
        return 0.0

    def _parse_memory(self, output: str) -> float:
        """Parse memory usage from free output."""
        lines = output.strip().split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 3:
                total = int(parts[1])
                used = int(parts[2])
                return (used / total) * 100 if total > 0 else 0.0
        return 0.0

    def _parse_disk(self, output: str) -> float:
        """Parse disk usage from df output."""
        lines = output.strip().split('\n')
        if len(lines) >= 2:
            parts = lines[1].split()
            if len(parts) >= 5:
                usage_str = parts[4].replace('%', '')
                return float(usage_str)
        return 0.0


# Example usage
monitor = SystemMonitor()
metrics = monitor.collect_metrics()

print(f"Timestamp: {metrics.timestamp}")
print(f"CPU Usage: {metrics.cpu_usage:.1f}%")
print(f"Memory Usage: {metrics.memory_usage:.1f}%")
print(f"Disk Usage: {metrics.disk_usage:.1f}%")
```

### Git Repository Analyzer

```python
from pyutilkit.subprocess import run_command
from pathlib import Path
from dataclasses import dataclass


@dataclass
class RepoInfo:
    """Git repository information."""
    branch: str
    commit: str
    status: str
    has_changes: bool


class GitAnalyzer:
    """Analyze git repositories."""

    def __init__(self, repo_path: Path):
        self.repo_path = repo_path

    def get_repo_info(self) -> RepoInfo:
        """Get comprehensive repository information."""
        # Get current branch
        branch_result = run_command(
            ["git", "branch", "--show-current"],
            cwd=self.repo_path
        )
        branch = branch_result.stdout.decode().strip()

        # Get current commit
        commit_result = run_command(
            ["git", "rev-parse", "HEAD"],
            cwd=self.repo_path
        )
        commit = commit_result.stdout.decode().strip()

        # Check for changes
        status_result = run_command(
            ["git", "status", "--porcelain"],
            cwd=self.repo_path
        )
        status_output = status_result.stdout.decode().strip()
        has_changes = len(status_output) > 0

        return RepoInfo(
            branch=branch or "DETACHED",
            commit=commit,
            status=status_output,
            has_changes=has_changes
        )

    def get_commit_history(self, count: int = 10) -> list[dict]:
        """Get recent commit history."""
        result = run_command(
            [
                "git", "log",
                f"-{count}",
                "--format=%H|%s|%an|%ad",
                "--date=short"
            ],
            cwd=self.repo_path
        )

        commits = []
        for line in result.stdout.decode().strip().split('\n'):
            if line:
                parts = line.split('|')
                if len(parts) == 4:
                    commits.append({
                        'hash': parts[0],
                        'message': parts[1],
                        'author': parts[2],
                        'date': parts[3]
                    })

        return commits

    def is_clean(self) -> bool:
        """Check if repository has no uncommitted changes."""
        info = self.get_repo_info()
        return not info.has_changes


# Example usage
analyzer = GitAnalyzer(Path("."))
info = analyzer.get_repo_info()

print(f"Branch: {info.branch}")
print(f"Commit: {info.commit[:8]}")
print(f"Has changes: {info.has_changes}")

if info.has_changes:
    print("\nUncommitted changes:")
    print(info.status)

print("\nRecent commits:")
for commit in analyzer.get_commit_history(5):
    print(f"  {commit['hash'][:8]} - {commit['message']} ({commit['date']})")
```

### Deployment Automation

```python
from pyutilkit.subprocess import run_command
from pathlib import Path


class Deployer:
    """Automated deployment tool."""

    def __init__(self, app_dir: Path, remote_host: str):
        self.app_dir = app_dir
        self.remote_host = remote_host

    def deploy(self) -> bool:
        """Deploy application to remote server."""
        print("Starting deployment...")

        # Step 1: Verify clean repository
        if not self._verify_clean_repo():
            print("✗ Repository has uncommitted changes")
            return False

        # Step 2: Run tests
        if not self._run_tests():
            print("✗ Tests failed")
            return False

        # Step 3: Build application
        if not self._build_app():
            print("✗ Build failed")
            return False

        # Step 4: Deploy to server
        if not self._deploy_to_server():
            print("✗ Deployment failed")
            return False

        # Step 5: Verify deployment
        if not self._verify_deployment():
            print("✗ Deployment verification failed")
            return False

        print("✓ Deployment successful!")
        return True

    def _verify_clean_repo(self) -> bool:
        """Verify repository is clean."""
        result = run_command(
            ["git", "status", "--porcelain"],
            cwd=self.app_dir
        )
        return len(result.stdout.decode().strip()) == 0

    def _run_tests(self) -> bool:
        """Run test suite."""
        result = run_command(
            ["uv", "run", "pytest", "-v"],
            cwd=self.app_dir
        )
        return result.returncode == 0

    def _build_app(self) -> bool:
        """Build application."""
        result = run_command(
            ["uv", "build"],
            cwd=self.app_dir
        )
        return result.returncode == 0

    def _deploy_to_server(self) -> bool:
        """Deploy built artifacts to server."""
        # Example using rsync
        result = run_command([
            "rsync", "-avz",
            "dist/",
            f"{self.remote_host}:/opt/app/"
        ])
        return result.returncode == 0

    def _verify_deployment(self) -> bool:
        """Verify deployment on remote server."""
        result = run_command([
            "ssh", self.remote_host,
            "systemctl is-active myapp"
        ])
        return result.returncode == 0 and b"active" in result.stdout


# Example usage
deployer = Deployer(
    app_dir=Path("/path/to/app"),
    remote_host="user@production.example.com"
)

success = deployer.deploy()
if not success:
    print("Deployment aborted due to errors")
```

## Common Pitfalls

!!! warning "Shell Injection"
    When passing commands as strings, be careful of shell injection vulnerabilities. Always prefer list format `["command", "arg1", "arg2"]` over string format `"command arg1 arg2"` when possible.

!!! warning "Large Output"
    For commands that produce very large output, consider redirecting to files instead of capturing in memory. The current implementation stores all output in memory.

!!! tip "Timeout Handling"
    For long-running commands, implement timeout logic by checking `result.elapsed` or using external timeout mechanisms.

!!! tip "Cross-Platform Compatibility"
    Remember that shell commands may differ between operating systems. Use platform-specific commands or cross-platform alternatives when possible.

## API Reference

::: pyutilkit.subprocess
    handler: python
    options:
      show_root_heading: true
      show_source: false
      members:
        - run_command
        - ProcessOutput
