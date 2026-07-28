# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

### Added

- `handle_exceptions` now accepts `log_args=False` to keep function arguments
  out of exception logs while retaining the function name, exception type, and
  traceback.

### Fixed

- Explicit `force_sgr=False` and `force_prefix=False` arguments now override
  truthy terminal environment settings, allowing callers to disable forced
  formatting.
- `run_command` no longer crashes when stdout or stderr is redirected to a
  text-only stream without a binary buffer; output remains captured while live
  echo is skipped for that stream.
- `hash_file` now rejects zero and negative buffer sizes instead of returning
  the empty-input digest or reading the entire file into memory.
- Re-entering a running `Stopwatch` now raises a clear `RuntimeError` instead
  of corrupting its state and later failing with `AttributeError`.
- Printing an empty `SGROutput` now emits its line terminator, matching builtin
  `print()` behavior.
- `run_command` now preserves every stdout and stderr echo failure in the
  raised exception's cause chain instead of silently discarding all but one.

## [0.12.0] - 2026-07-25

### Added

- `Timing` now accepts `hours` and `minutes` keyword arguments in addition to the existing duration units.

### Changed

- Renamed `TRUE_VAR` to `TRUTHY_VALUES` and changed its contents from falsy to truthy strings (`{"1", "true", "yes"}`) to fix inverted env-var behavior.
- `run_command` now requires an argument list (`list[str]`) and rejects ambiguous string commands instead of appearing to support shell syntax.
- `Stopwatch.average`, `.min`, and `.max` now consistently raise `ValueError("No laps recorded")` when no laps are available; `.average` previously raised `ZeroDivisionError`.

### Fixed

- `PY_UTIL_FORCE_SGR` and `PY_UTIL_FORCE_PREFIX` now work as documented: setting them to `1`, `true`, or `yes` (case-insensitive) enables forcing; setting them to `0`, `false`, or `no` disables it. Previously, `1`/`true`/`yes` had no effect while `0`/`false`/`no` enabled forcing.
- `run_command` now drains stdout and stderr concurrently, preventing pipe-buffer deadlocks while preserving real-time output and captured results.
- `run_command` now closes its pipes and reaps the child before propagating parent-stream write failures.
- Corrected the documented `Timing` output for durations expressed in minutes.
- `handle_exceptions` now rejects unsupported log levels when the decorator is applied, preventing configuration errors from masking exceptions raised by the wrapped function.
- Corrected the terminal usage guide's TTY handling, output routing, environment overrides, `full_color` example, and composite-output examples.
- `SGRString.print()` and `SGROutput.print()` now default `end` to `"\n"` instead of `os.linesep`, preventing `\r\r\n` on Windows text streams that already translate `\n`.
- `SGRString.header()` now preserves `is_error`, `force_prefix`, and `force_sgr` on its padded copy instead of resetting them.
- `SGROutput.header()` now raises `ValueError("Exactly one string is required for the header")` for an empty output instead of an `IndexError`.
- `Timing` now rounds its total to an integer number of nanoseconds instead of silently producing a float-valued `nanoseconds` that broke formatting and equality. A `UserWarning` is emitted only when rounding actually discards precision (e.g. `nanoseconds=1.5`); a `float` duration that lands on a whole nanosecond (e.g. `seconds=1.0`) is treated identically to its `int` equivalent, with no warning.

## [0.11.0] - 2025-11-10

### Added

- Added subtraction and negation to timing
- Added iter, min, max, len for Stopwatch instances.
- Added reset method to Stopwatch

### Changed

- Dropped support for python 3.9

### Fixed

- Made Singleton metaclass thread-safe

## [0.10.0] - 2024-12-09

### Added

- Allow passing any object to SGROutput

### Fixed

- Change the default line separator to an OS agnostic one
- Removed extra reset SGR code

## [0.9.0] - 2024-12-09

### Changed

- SGRString is now a dataclass not a string

### Fixed

- Timing \_\_truediv\_\_ doesn't perform a floor division any more

## [0.8.0] - 2024-12-05

### Changed

- SGRString always keeps the codes when turned to string, it can only lose them in printing outside a tty
- Simplified the run_command

## [0.7.0] - 2024-11-13

### Fixed

- Fixed missing windows timezones

## [0.6.0] - 2024-10-12

### Added

- Optionally suppress SGR codes

### Fixed

- Fixed printing issues with printing pseudo-terminals

## [0.5.0] - 2024-08-16

### Added

- A method to run a subprocess, and show the real time stdout and stderr and capture it

### Changed

- Changed license to BSD 3-Clause

## [0.4.0] - 2024-05-17

### Added

- Allowed operations between timings

### Fixed

- Allowed stopwatch to keep track of all the laps
- Improved Timing output for timings more than 1 minute.git

## [0.3.0] - 2024-05-14

### Added

- A Stopwatch class

### Fixed

- Fixed python version dependency

### Removed

- Removed the `__version__` from `__init__.py`

## [0.2.0] - 2024-05-13

### Added

- A method to handle exceptions
- A method to hash files

### Changed

- SGR string has the header as a method

## [0.1.0] - 2024-05-12

### Added

- A class to hold an SGR string
- A method to print a header spanning the whole terminal line
- A class to hold timings with ns resolution
- A metaclass for singletons
- A collection of date/datetime utils

[Keep a Changelog]: https://keepachangelog.com/en/1.1.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html
[Unreleased]: https://github.com/spapanik/pyutilkit/compare/v0.12.0...main
[0.12.0]: https://github.com/spapanik/pyutilkit/compare/v0.11.0...v0.12.0
[0.11.0]: https://github.com/spapanik/pyutilkit/compare/v0.10.0...v0.11.0
[0.10.0]: https://github.com/spapanik/pyutilkit/compare/v0.9.0...v0.10.0
[0.9.0]: https://github.com/spapanik/pyutilkit/compare/v0.8.0...v0.9.0
[0.8.0]: https://github.com/spapanik/pyutilkit/compare/v0.7.0...v0.8.0
[0.7.0]: https://github.com/spapanik/pyutilkit/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/spapanik/pyutilkit/compare/v0.5.0...v0.6.0
[0.5.0]: https://github.com/spapanik/pyutilkit/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/spapanik/pyutilkit/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/spapanik/pyutilkit/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/spapanik/pyutilkit/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/spapanik/pyutilkit/releases/tag/v0.1.0
