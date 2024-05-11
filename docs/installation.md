# Installation

# Using pip

[pip] is a package manager for Python.
You can use it to install `pyutilkit` and try it out:

```console
$ pip install pyutilkit
```

# Using poetry

[poetry] is a tool for managing Python project dependencies, and is the recommended way
to add `pyutilkit` to your project's dependencies. If you want to do so, you can do it
with the following command:

```console
$ poetry add pyutilkit
```

Or you can add `pyutilkit` to your `pyproject.toml` file:

```toml
[tool.poetry.dependencies]
pyutilkit = "^0.1"
```

## Python Version Requirement

Please note that `pyutilkit` requires Python 3.9 or higher. Please ensure
that you have such a version installed in your system. If not,
consider using a tool like [pyenv] to create a shell with the required Python version.

[pip]: https://pip.pypa.io/en/stable/
[poetry]: https://python-poetry.org/
[pyenv]: https://github.com/pyenv/pyenv
