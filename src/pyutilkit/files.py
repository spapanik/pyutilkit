from __future__ import annotations

import hashlib
import logging
from functools import wraps
from typing import TYPE_CHECKING, Literal, ParamSpec, TypeVar, cast

if TYPE_CHECKING:
    from collections.abc import Callable
    from pathlib import Path

logger = logging.getLogger(__name__)
INGEST_ERROR = "Function `%s` threw `%s` when called with args=%s and kwargs=%s"
R_co = TypeVar("R_co", covariant=True)
P = ParamSpec("P")
LogLevel = Literal["debug", "info", "warning", "error", "critical", "exception"]
LOG_LEVELS = frozenset({"debug", "info", "warning", "error", "critical", "exception"})


def _validate_log_level(log_level: object) -> LogLevel:
    if not isinstance(log_level, str) or log_level not in LOG_LEVELS:
        supported = ", ".join(sorted(LOG_LEVELS))
        msg = f"Unsupported log level {log_level!r}; expected one of: {supported}"
        raise ValueError(msg)
    return cast("LogLevel", log_level)


def handle_exceptions(
    *,
    exceptions: tuple[type[Exception], ...] = (Exception,),
    default: R_co | None = None,
    log_level: LogLevel = "info",
) -> Callable[[Callable[P, R_co]], Callable[P, R_co | None]]:
    log = getattr(logger, _validate_log_level(log_level))

    def decorator(func: Callable[P, R_co]) -> Callable[P, R_co | None]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R_co | None:
            try:
                return func(*args, **kwargs)
            except exceptions as exc:
                log(
                    INGEST_ERROR,
                    func.__name__,  # ty: ignore[unresolved-attribute]
                    exc.__class__.__name__,
                    args,
                    kwargs,
                    exc_info=True,
                )
                return default

        return wrapper

    return decorator


def hash_file(path: Path, buffer_size: int = 2**16) -> str:
    sha256 = hashlib.sha256()

    with path.open("rb") as f:
        while data := f.read(buffer_size):
            sha256.update(data)

    return sha256.hexdigest()
