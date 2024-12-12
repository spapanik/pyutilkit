import os
import sys
from unittest import mock

import pytest

from pyutilkit.term import SGRCodes, SGROutput, SGRString


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


@mock.patch("pyutilkit.term.print", new_callable=mock.MagicMock(spec=print))
@mock.patch("pyutilkit.term.sys.stdout", new=mock.MagicMock(spec=sys.stdout))
def test_sgr_string_print(mock_print: mock.MagicMock) -> None:
    sgr_string = SGRString(
        "*", params=[SGRCodes.BOLD, SGRCodes.RED], prefix="x", suffix="x"
    )
    sgr_string.print()
    assert mock_print.call_count == 1

    calls = [
        mock.call(
            "x",
            "\x1b[1m\x1b[31m",
            "*",
            "\x1b[0m",
            "x",
            sep="",
            end=os.linesep,
            file=sys.stdout,
        )
    ]
    assert mock_print.call_args_list == calls


@mock.patch("pyutilkit.term.print", new_callable=mock.MagicMock(spec=print))
@mock.patch("pyutilkit.term.sys.stdout", new=mock.MagicMock(spec=sys.stdout))
def test_sgr_string_print_full_color(mock_print: mock.MagicMock) -> None:
    sgr_string = SGRString(
        "*", params=[SGRCodes.BOLD, SGRCodes.RED], prefix="x", suffix="x"
    )
    sgr_string.print(full_color=True)
    assert mock_print.call_count == 1

    calls = [
        mock.call(
            "\x1b[1m\x1b[31m",
            "x",
            "*",
            "x",
            "\x1b[0m",
            sep="",
            end=os.linesep,
            file=sys.stdout,
        )
    ]
    assert mock_print.call_args_list == calls


@mock.patch("pyutilkit.term.print", new_callable=mock.MagicMock(spec=print))
@mock.patch("pyutilkit.term.sys.stdout", new=mock.MagicMock(spec=sys.stdout))
def test_sgr_output_print(mock_print: mock.MagicMock) -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string_2 = SGRString("Hello, World!", params=[SGRCodes.ITALIC, SGRCodes.BLUE])
    output = SGROutput([sgr_string_1, sgr_string_2])
    output.print()
    assert mock_print.call_count == 2
    calls = [
        mock.call(
            "",
            "\x1b[1m\x1b[31m",
            "Hello, World!",
            "\x1b[0m",
            "",
            sep="",
            end="",
            file=sys.stdout,
        ),
        mock.call(
            "",
            "\x1b[3m\x1b[34m",
            "Hello, World!",
            "\x1b[0m",
            "",
            sep="",
            end=os.linesep,
            file=sys.stdout,
        ),
    ]
    assert mock_print.call_args_list == calls


@mock.patch("pyutilkit.term.print", new_callable=mock.MagicMock(spec=print))
@mock.patch("pyutilkit.term.sys.stdout", new=mock.MagicMock(spec=sys.stdout))
def test_sgr_output_header(mock_print: mock.MagicMock) -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    output = SGROutput([sgr_string_1])
    output.header()
    assert mock_print.call_count == 1


def test_sgr_output_header_multi_string() -> None:
    sgr_string_1 = SGRString("Hello, World!", params=[SGRCodes.BOLD, SGRCodes.RED])
    sgr_string_2 = SGRString("Hello, World!", params=[SGRCodes.ITALIC, SGRCodes.BLUE])
    output = SGROutput([sgr_string_1, sgr_string_2])
    with pytest.raises(ValueError, match="Only one string is allowed for the header"):
        output.header()
