import os
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
        (False, False, False, f"*{os.linesep}", ""),
        (True, False, False, f"\x1b[1m\x1b[31m*\x1b[0m{os.linesep}", ""),
        (False, True, False, f"x*x{os.linesep}", ""),
        (True, True, False, f"x\x1b[1m\x1b[31m*\x1b[0mx{os.linesep}", ""),
        (False, False, True, "", f"*{os.linesep}"),
        (True, False, True, "", f"\x1b[1m\x1b[31m*\x1b[0m{os.linesep}"),
        (False, True, True, "", f"x*x{os.linesep}"),
        (True, True, True, "", f"x\x1b[1m\x1b[31m*\x1b[0mx{os.linesep}"),
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
    assert captured.out == f"\x1b[1m\x1b[31mx*x\x1b[0m{os.linesep}"
    assert captured.err == ""


def test_sgr_output_print(capsys: mock.MagicMock) -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string_2 = SGRString("Hello, World!", params=[SGRCodes.ITALIC, SGRCodes.BLUE])
    output = SGROutput([sgr_string_1, sgr_string_2], force_sgr=True, force_prefix=True)
    output.print()
    captured = capsys.readouterr()
    expected = (
        "\x1b[1m\x1b[31m"
        "Hello, World!"
        "\x1b[0m\x1b[3m\x1b[34m"
        "Hello, World!"
        f"\x1b[0m{os.linesep}"
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
        "\x1b[1m\x1b[31m"
        "Hello, World!"
        "\x1b[0m\x1b[3m\x1b[34m"
        "Hello, World!"
        f"\x1b[0m{os.linesep}"
    )
    assert captured.out == expected
    assert captured.err == ""


def test_sgr_output_header(capsys: mock.MagicMock) -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    output = SGROutput([sgr_string_1])
    output.header()
    captured = capsys.readouterr()
    assert captured.out == f"Hello, World!{os.linesep}"
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
    assert captured.out == f"Hello, World!{os.linesep}"
    assert captured.err == ""


def test_sgr_output_header_multi_string() -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string_2 = SGRString("Hello, World!", params=[SGRCodes.ITALIC, SGRCodes.BLUE])
    output = SGROutput([sgr_string_1, sgr_string_2])
    with pytest.raises(ValueError, match="Only one string is allowed for the header"):
        output.header()


def test_sgr_output_print_objects(capsys: mock.MagicMock) -> None:
    output = SGROutput([1, None])
    output.print()
    captured = capsys.readouterr()
    assert captured.out == f"1None{os.linesep}"
    assert captured.err == ""
