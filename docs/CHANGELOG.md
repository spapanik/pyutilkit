# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

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
[Unreleased]: https://github.com/spapanik/pyutilkit/compare/v0.10.0...main
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
