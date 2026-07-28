from typing import NamedTuple
from unittest import mock

import pytest

from pyutilkit.term import SGRCodes, SGROutput, SGRString


class TerminalSize(NamedTuple):
    columns: int
    lines: int


def test_sgr_string() -> None:
    string = "Hello, World!"
    sgr_string = SGRString(string, params=[SGRCodes.BOLD, SGRCodes.RED])
    assert str(sgr_string) == "\x1b[1m\x1b[31mHello, World!\x1b[0m"


def test_sgr_string_with_default() -> None:
    string = "Hello, World!"
    sgr_string = SGRString(string)
    assert str(sgr_string) == "Hello, World!"


def test_sgr_string_length() -> None:
    string = "Hello, World"
    sgr_string = SGRString(string, prefix="¡", suffix="!")
    assert len(sgr_string) == 14


def test_sgr_string_multiplication() -> None:
    sgr_string = SGRString(
        "*", params=[SGRCodes.BOLD, SGRCodes.RED], prefix="x", suffix="x"
    )
    sgr_string_mul = sgr_string * 3
    assert str(sgr_string_mul) == "x\x1b[1m\x1b[31m***\x1b[0mx"
    with pytest.raises(TypeError):
        sgr_string * "1"


def test_sgr_string_right_multiplication() -> None:
    sgr_string = SGRString(
        "*", params=[SGRCodes.BOLD, SGRCodes.RED], prefix="x", suffix="x"
    )
    sgr_string_mul = sgr_string * 3
    sgr_string_rmul = 3 * sgr_string
    assert str(sgr_string_rmul) == str(sgr_string_mul)
    with pytest.raises(TypeError):
        "1" * sgr_string


@pytest.mark.parametrize(
    ("force_sgr", "force_prefix", "is_error", "expected_stdout", "excepted_stderr"),
    [
        (False, False, False, "*\n", ""),
        (True, False, False, "\x1b[1m\x1b[31m*\x1b[0m\n", ""),
        (False, True, False, "x*x\n", ""),
        (True, True, False, "x\x1b[1m\x1b[31m*\x1b[0mx\n", ""),
        (False, False, True, "", "*\n"),
        (True, False, True, "", "\x1b[1m\x1b[31m*\x1b[0m\n"),
        (False, True, True, "", "x*x\n"),
        (True, True, True, "", "x\x1b[1m\x1b[31m*\x1b[0mx\n"),
    ],
)
def test_sgr_string_print(
    force_sgr: bool,
    force_prefix: bool,
    is_error: bool,
    expected_stdout: str,
    excepted_stderr: str,
    capsys: mock.MagicMock,
) -> None:
    sgr_string = SGRString(
        "*",
        params=[SGRCodes.BOLD, SGRCodes.RED],
        prefix="x",
        suffix="x",
        force_sgr=force_sgr,
        force_prefix=force_prefix,
        is_error=is_error,
    )
    sgr_string.print()
    captured = capsys.readouterr()
    assert captured.out == expected_stdout
    assert captured.err == excepted_stderr


def test_sgr_string_print_full_color(capsys: mock.MagicMock) -> None:
    sgr_string = SGRString(
        "*",
        params=[SGRCodes.BOLD, SGRCodes.RED],
        prefix="x",
        suffix="x",
        force_sgr=True,
        force_prefix=True,
    )
    sgr_string.print(full_color=True)
    captured = capsys.readouterr()
    assert captured.out == "\x1b[1m\x1b[31mx*x\x1b[0m\n"
    assert captured.err == ""


def test_sgr_output_print(capsys: mock.MagicMock) -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string_2 = SGRString("Hello, World!", params=[SGRCodes.ITALIC, SGRCodes.BLUE])
    output = SGROutput([sgr_string_1, sgr_string_2], force_sgr=True, force_prefix=True)
    output.print()
    captured = capsys.readouterr()
    expected = (
        "\x1b[1m\x1b[31mHello, World!\x1b[0m\x1b[3m\x1b[34mHello, World!\x1b[0m\n"
    )
    assert captured.out == expected
    assert captured.err == ""


@mock.patch("sys.stdout.isatty", new=mock.MagicMock(return_value=True))
def test_sgr_output_print_when_stdout_is_a_tty(capsys: mock.MagicMock) -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string_2 = SGRString("Hello, World!", params=[SGRCodes.ITALIC, SGRCodes.BLUE])
    output = SGROutput([sgr_string_1, sgr_string_2])
    output.print()
    captured = capsys.readouterr()
    expected = (
        "\x1b[1m\x1b[31mHello, World!\x1b[0m\x1b[3m\x1b[34mHello, World!\x1b[0m\n"
    )
    assert captured.out == expected
    assert captured.err == ""


def test_sgr_output_header(capsys: mock.MagicMock) -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    output = SGROutput([sgr_string_1])
    output.header()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"
    assert captured.err == ""


@pytest.mark.parametrize("columns", [80, 5])
def test_sgr_output_header_with_a_tty(columns: int, capsys: mock.MagicMock) -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    output = SGROutput([sgr_string_1])
    with mock.patch(
        "os.get_terminal_size",
        new=mock.MagicMock(return_value=TerminalSize(columns, 24)),
    ):
        output.header()
    captured = capsys.readouterr()
    assert captured.out == "Hello, World!\n"
    assert captured.err == ""


def test_sgr_output_header_multi_string() -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string_2 = SGRString("Hello, World!", params=[SGRCodes.ITALIC, SGRCodes.BLUE])
    output = SGROutput([sgr_string_1, sgr_string_2])
    with pytest.raises(
        ValueError, match="Exactly one string is required for the header"
    ):
        output.header()


def test_sgr_output_header_empty() -> None:
    output = SGROutput([])
    with pytest.raises(
        ValueError, match="Exactly one string is required for the header"
    ):
        output.header()


def test_sgr_string_header_preserves_state_early_return(
    capsys: mock.MagicMock,
) -> None:
    sgr_string = SGRString(
        "Hello, World!",
        params=[SGRCodes.BOLD, SGRCodes.RED],
        force_sgr=True,
        force_prefix=True,
        is_error=True,
    )
    with mock.patch("os.get_terminal_size", side_effect=OSError):
        sgr_string.header()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "\x1b[1m\x1b[31mHello, World!\x1b[0m\n"


def test_sgr_string_header_preserves_state_padded(capsys: mock.MagicMock) -> None:
    sgr_string = SGRString(
        "Hi",
        params=[SGRCodes.BOLD, SGRCodes.RED],
        force_sgr=True,
        force_prefix=True,
        is_error=True,
    )
    with mock.patch(
        "os.get_terminal_size",
        new=mock.MagicMock(return_value=TerminalSize(10, 24)),
    ):
        sgr_string.header()
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == "    \x1b[1m\x1b[31mHi\x1b[0m    \n"


def test_sgr_output_print_objects(capsys: mock.MagicMock) -> None:
    output = SGROutput([1, None])
    output.print()
    captured = capsys.readouterr()
    assert captured.out == "1None\n"
    assert captured.err == ""


@pytest.mark.parametrize(
    "env_value",
    ["1", "true", "yes", "TRUE", "True", "YES"],
)
def test_force_sgr_via_env_truthy(
    env_value: str, monkeypatch: pytest.MonkeyPatch, capsys: mock.MagicMock
) -> None:
    monkeypatch.setenv("PY_UTIL_FORCE_SGR", env_value)
    sgr_string = SGRString("*", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string.print()
    captured = capsys.readouterr()
    assert captured.out == "\x1b[1m\x1b[31m*\x1b[0m\n"


@pytest.mark.parametrize(
    "env_value",
    ["0", "false", "no", "FALSE", "False", "NO"],
)
def test_force_sgr_via_env_falsy(
    env_value: str, monkeypatch: pytest.MonkeyPatch, capsys: mock.MagicMock
) -> None:
    monkeypatch.setenv("PY_UTIL_FORCE_SGR", env_value)
    sgr_string = SGRString("*", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string.print()
    captured = capsys.readouterr()
    assert captured.out == "*\n"


def test_force_sgr_via_env_unset(capsys: mock.MagicMock) -> None:
    sgr_string = SGRString("*", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string.print()
    captured = capsys.readouterr()
    assert captured.out == "*\n"


@pytest.mark.parametrize(
    "env_value",
    ["1", "true", "yes", "TRUE", "True", "YES"],
)
def test_force_prefix_via_env_truthy(
    env_value: str, monkeypatch: pytest.MonkeyPatch, capsys: mock.MagicMock
) -> None:
    monkeypatch.setenv("PY_UTIL_FORCE_PREFIX", env_value)
    sgr_string = SGRString("*", prefix="x", suffix="x")
    sgr_string.print()
    captured = capsys.readouterr()
    assert captured.out == "x*x\n"


@pytest.mark.parametrize(
    "env_value",
    ["0", "false", "no", "FALSE", "False", "NO"],
)
def test_force_prefix_via_env_falsy(
    env_value: str, monkeypatch: pytest.MonkeyPatch, capsys: mock.MagicMock
) -> None:
    monkeypatch.setenv("PY_UTIL_FORCE_PREFIX", env_value)
    sgr_string = SGRString("*", prefix="x", suffix="x")
    sgr_string.print()
    captured = capsys.readouterr()
    assert captured.out == "*\n"


def test_force_prefix_via_env_unset(capsys: mock.MagicMock) -> None:
    sgr_string = SGRString("*", prefix="x", suffix="x")
    sgr_string.print()
    captured = capsys.readouterr()
    assert captured.out == "*\n"


def test_force_sgr_constructor_overrides_env(
    monkeypatch: pytest.MonkeyPatch, capsys: mock.MagicMock
) -> None:
    monkeypatch.setenv("PY_UTIL_FORCE_SGR", "0")
    sgr_string = SGRString("*", params=[SGRCodes.BOLD, SGRCodes.RED], force_sgr=True)
    sgr_string.print()
    captured = capsys.readouterr()
    assert captured.out == "\x1b[1m\x1b[31m*\x1b[0m\n"


def test_force_prefix_constructor_overrides_env(
    monkeypatch: pytest.MonkeyPatch, capsys: mock.MagicMock
) -> None:
    monkeypatch.setenv("PY_UTIL_FORCE_PREFIX", "0")
    sgr_string = SGRString("*", prefix="x", suffix="x", force_prefix=True)
    sgr_string.print()
    captured = capsys.readouterr()
    assert captured.out == "x*x\n"


@pytest.mark.parametrize("use_output", [False, True])
def test_force_sgr_constructor_can_disable_env(
    use_output: bool,
    monkeypatch: pytest.MonkeyPatch,
    capsys: mock.MagicMock,
) -> None:
    monkeypatch.setenv("PY_UTIL_FORCE_SGR", "1")
    string = SGRString("*", params=[SGRCodes.BOLD, SGRCodes.RED])
    output = SGROutput([string], force_sgr=False) if use_output else string
    if not use_output:
        output = SGRString("*", params=[SGRCodes.BOLD, SGRCodes.RED], force_sgr=False)
    output.print()
    captured = capsys.readouterr()
    assert captured.out == "*\n"


@pytest.mark.parametrize("use_output", [False, True])
def test_force_prefix_constructor_can_disable_env(
    use_output: bool,
    monkeypatch: pytest.MonkeyPatch,
    capsys: mock.MagicMock,
) -> None:
    monkeypatch.setenv("PY_UTIL_FORCE_PREFIX", "1")
    string = SGRString("*", prefix="x", suffix="x")
    output = SGROutput([string], force_prefix=False) if use_output else string
    if not use_output:
        output = SGRString("*", prefix="x", suffix="x", force_prefix=False)
    output.print()
    captured = capsys.readouterr()
    assert captured.out == "*\n"
