from __future__ import annotations

import os
from collections.abc import Iterable
from enum import IntEnum, unique
from math import ceil, floor
from typing import Any


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
    _sgr: str
    __slots__ = ("_sgr",)

    def __new__(cls, value: Any, *, params: Iterable[SGRCodes] = ()) -> SGRString:
        string = super().__new__(cls, value)
        suffix = SGRCodes.RESET.sequence
        prefix = "".join(param.sequence for param in params) or SGRCodes.RESET.sequence
        object.__setattr__(string, "_sgr", f"{prefix}{value}{suffix}")
        return string

    def __setattr__(self, name: str, value: Any) -> None:
        msg = "SGRString is immutable"
        raise AttributeError(msg)

    def __delattr__(self, name: str) -> None:
        msg = "SGRString is immutable"
        raise AttributeError(msg)

    def __str__(self) -> str:
        return self._sgr


def header(
    text: str, *, padding: str = " ", left_spaces: int = 1, right_spaces: int = 1
) -> None:
    columns = os.get_terminal_size().columns
    text = f"{' ' * left_spaces}{text.strip()}{' ' * right_spaces}"
    title_length = len(text)
    if title_length >= columns:
        print(text.strip())
        return

    half = (columns - len(text)) / 2
    print(f"{padding * ceil(half)}{text}{padding * floor(half)}")
