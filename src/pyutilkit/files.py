from __future__ import annotations

import logging
from collections.abc import Callable
from functools import wraps
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from typing_extensions import ParamSpec  # py3.9: import from typing

    P = ParamSpec("P")

logger = logging.getLogger(__name__)
INGEST_ERROR = "Function `%s` threw `%s` when called with args=%s and kwargs=%s"
R_co = TypeVar("R_co", covariant=True)


def handle_exceptions(
    *,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    default: R_co | None = None,
    log_level: str = "info",
) -> Callable[[Callable[P, R_co]], Callable[P, R_co | None]]:
    def decorator(func: Callable[P, R_co]) -> Callable[P, R_co | None]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R_co | None:
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                getattr(logger, log_level)(
                    INGEST_ERROR,
                    func.__name__,
                    exc.__class__.__name__,
                    args,
                    kwargs,
                    exc_info=True,
                )
                return default

        return wrapper

    return decorator
