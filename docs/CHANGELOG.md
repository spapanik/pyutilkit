# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog], and this project adheres to [Semantic Versioning].

## [Unreleased]

### Added

-   Allowed operations between timings

### Fixed

-   Improved Timing output for timings more than 1 minute.git

## [0.3.0] - 2024-05-14

### Added

-   A Stopwatch class

### Fixed

-   Fixed python version dependency

### Removed

-   Removed the `__version__` from `__init__.py`

## [0.2.0] - 2024-05-13

### Added

-   A method to handle exceptions
-   A method to hash files

### Changed

-   SGR string has the header as a method

## [0.1.0] - 2024-05-12

### Added

-   A class to hold an SGR string
-   A method to print a header spanning the whole terminal line
-   A class to hold timings with ns resolution
-   A metaclass for singletons
-   A collection of date/datetime utils

[Keep a Changelog]: https://keepachangelog.com/en/1.0.0/
[Semantic Versioning]: https://semver.org/spec/v2.0.0.html
[Unreleased]: https://github.com/spapanik/pyutilkit/compare/v0.3.0...main
[0.3.0]: https://github.com/spapanik/pyutilkit/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/spapanik/pyutilkit/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/spapanik/pyutilkit/releases/tag/v0.1.0
