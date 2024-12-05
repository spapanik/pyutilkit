import sys
from unittest import mock

import pytest

from pyutilkit.term import SGRCodes, SGRString


def test_sgr_string() -> None:
    string = "Hello, World!"
    sgr_string = SGRString(string, params=[SGRCodes.BOLD, SGRCodes.RED])
    assert repr(sgr_string) == "'Hello, World!'"
    assert str(sgr_string) == "\x1b[1m\x1b[31mHello, World!\x1b[0m"
    assert isinstance(sgr_string, str)


def test_sgr_string_with_default() -> None:
    string = "Hello, World!"
    sgr_string = SGRString(string)
    assert repr(sgr_string) == "'Hello, World!'"
    assert str(sgr_string) == "Hello, World!"
    assert isinstance(sgr_string, str)


def test_sgr_string_length() -> None:
    string = "Hello, World"
    sgr_string = SGRString(string, prefix="¡", suffix="!")
    assert len(sgr_string) == 14


def test_sgr_string_set_attribute() -> None:
    string = "Hello, World!"
    sgr_string = SGRString(string, params=[SGRCodes.BOLD, SGRCodes.RED])
    with pytest.raises(AttributeError):
        sgr_string._string = "Hello, World!"  # noqa: SLF001


def test_sgr_string_del_attribute() -> None:
    string = "Hello, World!"
    sgr_string = SGRString(string, params=[SGRCodes.BOLD, SGRCodes.RED])

    with pytest.raises(AttributeError):
        del sgr_string._sgr  # noqa: SLF001


def test_sgr_string_multiplication() -> None:
    sgr_string = SGRString(
        "*", params=[SGRCodes.BOLD, SGRCodes.RED], prefix="x", suffix="x"
    )
    sgr_string_mul = sgr_string * 3
    assert str(sgr_string_mul) == "x\x1b[1m\x1b[31m***\x1b[0mx"


def test_sgr_string_right_multiplication() -> None:
    sgr_string = SGRString(
        "*", params=[SGRCodes.BOLD, SGRCodes.RED], prefix="x", suffix="x"
    )
    sgr_string_mul = sgr_string * 3
    sgr_string_rmul = 3 * sgr_string
    assert str(sgr_string_rmul) == str(sgr_string_mul)


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
            end="\n",
            file=sys.stdout,
        )
    ]
    assert mock_print.call_args_list == calls
