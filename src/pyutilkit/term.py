from __future__ import annotations

import os
from enum import IntEnum, unique
from math import ceil, floor
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Iterable

    from typing_extensions import Self  # py3.10: import from typing


@unique
class SGRCodes(IntEnum):
    RESET = 0

    BOLD = 1
    ITALIC = 3
    UNDERLINE = 4
    BLINK = 5
    REVERSE = 7
    CONCEAL = 8

    BLACK = 30
    RED = 31
    GREEN = 32
    YELLOW = 33
    BLUE = 34
    MAGENTA = 35
    CYAN = 36
    GREY = 37

    BG_BLACK = 40
    BG_RED = 41
    BG_GREEN = 42
    BG_YELLOW = 43
    BG_BLUE = 44
    BG_MAGENTA = 45
    BG_CYAN = 46
    BG_GREY = 47

    BLACK_BRIGHT = 90
    RED_BRIGHT = 91
    GREEN_BRIGHT = 92
    YELLOW_BRIGHT = 93
    BLUE_BRIGHT = 94
    MAGENTA_BRIGHT = 95
    CYAN_BRIGHT = 96
    WHITE_BRIGHT = 97

    BG_BLACK_BRIGHT = 100
    BG_RED_BRIGHT = 101
    BG_GREEN_BRIGHT = 102
    BG_YELLOW_BRIGHT = 103
    BG_BLUE_BRIGHT = 104
    BG_MAGENTA_BRIGHT = 105
    BG_CYAN_BRIGHT = 106
    BG_WHITE_BRIGHT = 107

    @property
    def sequence(self) -> str:
        return f"\033[{self.value}m"


class SGRString(str):
    _sgr: tuple[SGRCodes, ...]
    _string: str
    __slots__ = ("_sgr", "_string")

    def __new__(cls, obj: Any, *, params: Iterable[SGRCodes] = ()) -> Self:
        string = super().__new__(cls, obj)
        object.__setattr__(string, "_string", str(obj))
        object.__setattr__(string, "_sgr", tuple(params))
        return string

    def __setattr__(self, name: str, value: Any) -> None:
        msg = "SGRString is immutable"
        raise AttributeError(msg)

    def __delattr__(self, name: str) -> None:
        msg = "SGRString is immutable"
        raise AttributeError(msg)

    def __str__(self) -> str:
        if not self._sgr or os.getenv("USE_SGR_CODES") in {"0", "false", "no"}:
            return self._string
        prefix = "".join(code.sequence for code in self._sgr)
        return f"{prefix}{self._string}{SGRCodes.RESET.sequence}"

    def __mul__(self, other: Any) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        return type(self)(self._string * other, params=self._sgr)

    def __rmul__(self, other: Any) -> Self:
        if not isinstance(other, int):
            return NotImplemented
        return type(self)(self._string * other, params=self._sgr)

    def header(
        self,
        *,
        padding: str = " ",
        left_spaces: int = 1,
        right_spaces: int = 1,
        space: str = " ",
    ) -> None:
        try:
            # in pseudo-terminals it throws OSError
            terminal_size = os.get_terminal_size()
        except OSError:
            columns = 80
        else:
            columns = terminal_size.columns
        text = f"{space * left_spaces}{self}{space * right_spaces}"
        title_length = left_spaces + len(self) + right_spaces
        if title_length >= columns:
            print(text.strip())
            return

        half = (columns - title_length) / 2
        print(f"{padding * ceil(half)}{text}{padding * floor(half)}")
