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
    assert str(sgr_string) == "\x1b[0mHello, World!\x1b[0m"
    assert isinstance(sgr_string, str)


def test_sgr_string_set_attribute() -> None:
    string = "Hello, World!"
    sgr_string = SGRString(string, params=[SGRCodes.BOLD, SGRCodes.RED])
    with pytest.raises(AttributeError):
        sgr_string._sgr = "Hello, World!"  # noqa: SLF001


def test_sgr_string_del_attribute() -> None:
    string = "Hello, World!"
    sgr_string = SGRString(string, params=[SGRCodes.BOLD, SGRCodes.RED])

    with pytest.raises(AttributeError):
        del sgr_string._sgr  # noqa: SLF001
